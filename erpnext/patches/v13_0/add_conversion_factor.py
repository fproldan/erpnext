# Copyright (c) 2020, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

def execute():
	doc = frappe.new_doc("UOM Conversion Factor")
	doc.category = "Length"
	doc.from_uom = "Metros"
	doc.to_uom = "Metros"
	doc.value = 1
	doc.save()
	frappe.db.commit()