# Copyright (c) 2021, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

import frappe


def execute():
    field = frappe.db.get_value("Custom Field", {"dt": "Payment Entry", "fieldname": 'gst_section'})
    if field:
        custom_field = frappe.get_doc("Custom Field", field)
		custom_field.flags.ignore_validate = True
        custom_field.hidden = 1
        custom_field.save()
        frappe.clear_cache(doctype="Payment Entry")
        frappe.db.updatedb("Payment Entry")
