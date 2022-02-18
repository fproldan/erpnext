from __future__ import unicode_literals

import frappe
import erpnext.hooks as hooks


def execute():
    hooks.after_migrate.append("erpnext.patches.v13_0.remove_report.delete_report")


def delete_report():
    frappe.flags.in_patch = True
    frappe.delete_doc('Report', 'Sales Payment Summary', ignore_missing=True, ignore_permissions=True)
