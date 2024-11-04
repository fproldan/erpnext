# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form


class ProcessSalesCommission(Document):
	def validate(self):
		self.validate_from_to_dates()
		self.validate_salary_component()

	def validate_from_to_dates(self):
		return super().validate_from_to_dates("from_date", "to_date")

	def validate_salary_component(self):
		if self.pay_via_salary and not frappe.db.get_single_value("Payroll Settings", "salary_component_for_sales_commission"):
			frappe.throw(_("Please set {0} in {1}").format(frappe.bold("Salary Component for Sales Commission"), get_link_to_form("Payroll Settings", "Payroll Settings")))

	def on_submit(self):
		self.make_sales_commission_document()

	def make_sales_commission_document(self):
		for sales_persons in self.sales_persons:
			doc = frappe.new_doc("Sales Commission")
			doc.sales_person = sales_persons.sales_person
			doc.commission_based_on = self.commission_based_on
			doc.from_date = self.from_date
			doc.to_date = self.to_date
			doc.pay_via_salary = self.pay_via_salary
			doc.process_sales_commission_reference = self.name
			doc.omit_sales_person_transactions = self.omit_sales_person_transactions
			doc.commission_against = self.commission_against
			doc.commission_against_filter = self.commission_against_filter
			doc.add_contributions(self.name)
			doc.insert()
			
			if self.submit_sales_commission:
				try:
					doc.submit()
				except Exception:
					frappe.log_error(title=f"Error al validar Comision De Ventas", message=frappe.get_traceback())
			
			if not frappe.db.get_single_value("Selling Settings", "approval_required_for_sales_commission_payout"):
				doc.reload()
				if self.pay_via_salary and doc.employee:
					if frappe.db.exists('Salary Structure Assignment', {'employee': doc.employee}):
						doc.submit()
						doc.payout_entry()

	@frappe.whitelist()
	def get_sales_persons(self):
		employee_filters = {"company": self.company}
		if self.department:
			employee_filters["department"] = self.department
		if self.designation:
			employee_filters["designation"] = self.designation
		if self.branch:
			employee_filters["branch"] = self.branch
		if self.grade:
			employee_filters["grade"] = self.grade

		employees = frappe.get_all("Employee", filters=employee_filters, pluck="name")
		for sales_person in frappe.get_all(
			"Sales Person",
			filters=[["employee", "in", employees]],
			fields="name as sales_person"
		):
			self.append("sales_persons", sales_person)