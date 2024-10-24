# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class PaymentTermsTemplate(Document):
	def validate(self):
		self.validate_invoice_portion()

	def validate_invoice_portion(self):
		total_portion = 0
		for term in self.terms:
			total_portion += flt(term.get('invoice_portion', 0))

		if flt(total_portion, 2) != 100.00:
			frappe.msgprint(_('Combined invoice portion must equal 100%'), raise_exception=1, indicator='red')
