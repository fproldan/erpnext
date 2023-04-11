# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VerificacionNOSIS(Document):
	
	def get_dias(self):
		from datetime import date
		delta = date.today() - self.fecha
		return delta.days
