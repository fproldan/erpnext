# Copyright (c) 2020, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

def execute():
	if frappe.db.exists("Domain", "BOM"):
		return

	d = frappe.new_doc('Domain')
	d.name = 'BOM'
	d.domain = 'BOM'
	d.save()
	frappe.db.commit()