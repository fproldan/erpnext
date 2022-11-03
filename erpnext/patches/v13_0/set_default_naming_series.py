from __future__ import unicode_literals

import frappe

def execute():
	for company_name in frappe.get_all('Company', pluck='name'):
		comp = frappe.get_doc('Company', company_name)
		comp.create_default_naming_series()

	frappe.db.commit()