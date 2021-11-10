from __future__ import unicode_literals

import frappe


def setup_support():
    add_custom_roles_for_reports()


def add_custom_roles_for_reports():
    for report in ['Support Hour Distribution', 'Issue Summary', 'Issue Analytics', 'First Response Time for Issues']:
        if not frappe.db.get_value('Custom Role', dict(report=report)):
            frappe.get_doc(dict(
                doctype='Custom Role',
                report=report,
                roles=[
                    dict(role='Support Team'),
                    dict(role='System Manager')
                ]
            )).insert()
