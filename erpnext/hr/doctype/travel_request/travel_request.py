# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.hr.utils import validate_active_employee


class TravelRequest(Document):
	def validate(self):
		validate_active_employee(self.employee)


@frappe.whitelist()
def make_employee_advance(dt, dn):
	travel_request = frappe.get_doc(dt, dn)
	employee_advance = frappe.new_doc('Employee Advance')
	employee_advance.employee = travel_request.employee
	employee_advance.advance_amount = sum(c.total_amount for c in travel_request.costings)
	employee_advance.purpose = travel_request.name
	employee_advance.travel_request = travel_request.name
	return employee_advance