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

	doc = frappe.new_doc("UOM Conversion Factor")
	doc.category = "Length"
	doc.from_uom = "Kilómetros"
	doc.to_uom = "Kilómetros"
	doc.value = 1
	doc.save()

	frappe.db.commit()
	doc = frappe.new_doc("UOM Conversion Factor")
	doc.category = "Length"
	doc.from_uom = "Centímetros"
	doc.to_uom = "Centímetros"
	doc.value = 1
	doc.save()

	frappe.db.commit()