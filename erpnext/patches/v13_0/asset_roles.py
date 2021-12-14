from __future__ import unicode_literals

import frappe


def execute():
    frappe.db.delete("Role", "Maintenance Manager")
    frappe.db.delete("Role", "Maintenance User")
