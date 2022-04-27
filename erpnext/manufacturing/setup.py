from __future__ import unicode_literals

import frappe


def setup_bom():
    add_custom_roles_for_reports()


def add_custom_roles_for_reports():
    for report in ['BOM Stock Report']:
        if not frappe.db.get_value('Custom Role', dict(report=report)):
            frappe.get_doc(dict(
                doctype='Custom Role',
                report=report,
                roles=[
                    dict(role='Manufacturing Manager'),
                    dict(role='Manufacturing User')
                ]
            )).insert()