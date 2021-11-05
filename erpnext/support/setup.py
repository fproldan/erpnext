from __future__ import unicode_literals

import frappe


def setup_support():
    add_custom_roles_for_reports()


def add_custom_roles_for_reports():
    if not frappe.db.get_value('Custom Role', dict(report='Support Hour Distribution')):
        frappe.get_doc(dict(
            doctype='Custom Role',
            report='Support Hour Distribution',
            roles= [
                dict(role='Support Team'),
                dict(role='System Manager')
            ]
        )).insert()
