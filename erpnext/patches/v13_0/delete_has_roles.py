from __future__ import unicode_literals

import frappe

def execute():
    frappe.db.delete('Has Role', {"role": ['in', ["Maintenance User", "Maintenance Manager"]]})
