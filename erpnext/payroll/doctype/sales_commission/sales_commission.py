# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import json
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form
from erpnext.accounts.general_ledger import make_gl_entries


class SalesCommission(Document):
	def validate(self):
		self.validate_from_to_dates()

		self.validate_salary_component()
		self.calculate_total_contribution_and_total_commission_amount()
		self.create_employee()

	def validate_from_to_dates(self):
		return super().validate_from_to_dates("from_date", "to_date")

	def validate_amount(self):
		if self.total_commission_amount <= 0:
			frappe.throw(_("Total Commission Amount should be greater than 0"))

	def validate_salary_component(self):
		if self.pay_via_salary and not frappe.db.get_single_value("Payroll Settings", "salary_component_for_sales_commission"):
			frappe.throw(_("Please set {0} in {1}").format(
				frappe.bold("Salary Component for Sales Commission"), get_link_to_form("Payroll Settings", "Payroll Settings")))

	def on_submit(self):
		self.validate_amount()
		self.make_gl_entries()
		self.db_set("status", "Unpaid")
	
	def on_cancel(self):
		self.ignore_linked_doctypes = ('GL Entry',)
		self.make_gl_entries(cancel=1)
	
	def add_party_gl_entries(self, gl_entries):
		return
		if self.party_account:
			if self.payment_type=="Receive":
				against_account = self.paid_to
			else:
				against_account = self.paid_from

			party_gl_dict = self.get_gl_dict({
				"account": self.party_account,
				"party_type": self.party_type,
				"party": self.party,
				"against": against_account,
				"account_currency": self.party_account_currency,
				"cost_center": self.cost_center
			}, item=self)

			dr_or_cr = "credit" if erpnext.get_party_account_type(self.party_type) == 'Receivable' else "debit"

			for d in self.get("references"):
				cost_center = self.cost_center
				if d.reference_doctype == "Sales Invoice" and not cost_center:
					cost_center = frappe.db.get_value(d.reference_doctype, d.reference_name, "cost_center")
				gle = party_gl_dict.copy()
				gle.update({
					"against_voucher_type": d.reference_doctype,
					"against_voucher": d.reference_name,
					"cost_center": cost_center
				})

				allocated_amount_in_company_currency = flt(flt(d.allocated_amount) * flt(d.exchange_rate),
					self.precision("paid_amount"))

				gle.update({
					dr_or_cr + "_in_account_currency": d.allocated_amount,
					dr_or_cr: allocated_amount_in_company_currency
				})

				gl_entries.append(gle)

			if self.unallocated_amount:
				exchange_rate = self.get_exchange_rate()
				base_unallocated_amount = (self.unallocated_amount * exchange_rate)

				gle = party_gl_dict.copy()

				gle.update({
					dr_or_cr + "_in_account_currency": self.unallocated_amount,
					dr_or_cr: base_unallocated_amount
				})

				gl_entries.append(gle)
	
	def make_gl_entries(self, cancel=0):
		gl_entries = []
		self.add_party_gl_entries(gl_entries)
		make_gl_entries(gl_entries, cancel=cancel)

	@frappe.whitelist()
	def add_contributions(self, process_sales_commission):
		self.set("contributions", [])
		filter_date = "transaction_date" if self.commission_based_on == "Sales Order" else "posting_date"
		customer_field = "customer" if self.commission_based_on != "Payment Entry" else "party"
		records = [entry.name for entry in frappe.db.get_all(self.commission_based_on, filters={"company": self.company, "docstatus": 1, filter_date: ('between', [self.from_date, self.to_date])})]
		sales_persons_details = frappe.get_all(
			"Sales Team", filters={"parent": ['in', records], "sales_person": self.sales_person},
			fields=["sales_person", "commission_rate", "incentives", "allocated_percentage", "allocated_amount", "parent"])
		if sales_persons_details:
			for record in sales_persons_details:
				if add_record(record, self.sales_person):
					record_details = frappe.db.get_value(self.commission_based_on, filters={"name": record["parent"]}, fieldname=[customer_field, filter_date], as_dict=True)
					contribution = {
						"document_type": self.commission_based_on,
						"order_or_invoice": record["parent"],
						"customer": record_details.get(customer_field),
						"posting_date": record_details[filter_date],
						"contribution_percent": record["allocated_percentage"],
						"contribution_amount": record["allocated_amount"],
						"commission_rate": record["commission_rate"],
						"commission_amount": record["incentives"],
						"process_sales_commission": process_sales_commission,
					}
					self.append("contributions", contribution)
		self.calculate_total_contribution_and_total_commission_amount()

	def calculate_total_contribution_and_total_commission_amount(self):
		total_contribution, total_commission_amount = 0, 0
		for entry in self.contributions:
			total_contribution += entry.contribution_amount
			total_commission_amount += entry.commission_amount

		if self.calculate_commission_manually:
			rate = self.commission_rate
			total_commission_amount = total_contribution * (rate / 100)

		self.total_contribution = total_contribution
		self.total_commission_amount = total_commission_amount

	@frappe.whitelist()
	def payout_entry(self, mode_of_payment=None, reference_no=None, reference_date=None):
		from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
		if mode_of_payment:
			paid_from = get_bank_cash_account(mode_of_payment, self.company).get("account")

		paid_to = frappe.db.get_value("Company", filters={"name": self.company}, fieldname=['default_payroll_payable_account'], as_dict=True)['default_payroll_payable_account']
		if not paid_to:
			frappe.throw(_("Ingresar la cuenta de pago de nómina predeterminada en {}").format(get_link_to_form("Company", self.company)))
		if self.pay_via_salary:
			self.make_additional_salary()
		else:
			self.make_payment_entry(mode_of_payment, paid_from, paid_to, reference_no, reference_date)

	def make_additional_salary(self):
		currency = frappe.get_value("Company", self.company, "default_currency")
		doc = frappe.new_doc("Additional Salary")
		doc.employee = self.employee
		doc.company = self.company
		doc.currency = currency
		doc.salary_component = frappe.db.get_single_value("Payroll Settings", "salary_component_for_sales_commission")
		doc.payroll_date = self.to_date
		doc.amount = self.total_commission_amount
		doc.ref_doctype = self.doctype
		doc.ref_docname = self.name

		doc.submit()

		self.db_set("reference_doctype", "Additional Salary")
		self.db_set("reference_name", doc.name)
		self.db_set("status", "Paid")

	def create_employee(self):
		from frappe.utils import nowdate

		if self.employee:
			return self.employee

		sales_person = frappe.get_doc("Sales Person", self.sales_person)
		employee = frappe.new_doc("Employee")
		employee.update({
			"first_name": sales_person.name,
			"gender": "Male",
			"date_of_birth": "1970-01-01",
			"date_of_joining": nowdate(),
		})
		employee.insert(ignore_permissions=True)
		sales_person.db_set("employee", employee.name)
		self.db_set("employee", employee.name)
		frappe.db.commit()

	def make_payment_entry(self, mode_of_payment, paid_from, paid_to, reference_no, reference_date):
		doc = frappe.new_doc("Payment Entry")
		doc.company = self.company
		doc.payment_type = "Pay"
		doc.mode_of_payment = mode_of_payment
		doc.reference_no = reference_no
		doc.reference_date = reference_date
		doc.party_type = "Employee"
		doc.party = self.employee
		doc.paid_from = paid_from
		doc.paid_to = paid_to
		doc.paid_amount = self.total_commission_amount
		doc.received_amount = self.total_commission_amount
		doc.source_exchange_rate = 1
		doc.target_exchange_rate = 1
		doc.set("references", [])
		self.add_references(doc)
		doc.submit()
		self.db_set("reference_doctype", "Payment Entry")
		self.db_set("reference_name", doc.name)
		self.db_set("status", "Paid")

	def add_references(self, doc):
		reference = {
			'reference_doctype': 'Sales Commission',
			'reference_name': self.name,
			'due_date': self.to_date,
			'total_amount': self.total_commission_amount,
			'outstanding_amount': self.total_commission_amount,
			'allocated_amount': self.total_commission_amount,
		}
		doc.append("references", reference)


def add_record(record, sales_person):
	previous_contibutions = frappe.get_all("Contributions", filters={"order_or_invoice": record["parent"], "docstatus": 1}, fields=["parent"])
	if previous_contibutions:
		for contributions in previous_contibutions:
			if frappe.db.get_value("Sales Commission", {"name": contributions["parent"]}, fieldname=["sales_person"]) == sales_person:
				return False
	return True


@frappe.whitelist()
def payout_entries(names, mode_of_payment=None, reference_no=None, reference_date=None):
	if not frappe.has_permission("Sales Commission", "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	names = json.loads(names)
	for name in names:
		sales_commission = frappe.get_doc("Sales Commission", name)
		if sales_commission.docstatus != 1 or sales_commission.status == 'Paid':
			continue

		sales_commission.payout_entry(mode_of_payment, reference_no, reference_date)

	frappe.local.message_log = []