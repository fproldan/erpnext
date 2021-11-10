from __future__ import unicode_literals

import frappe


def setup_projects():
    add_custom_roles_for_reports()


def add_custom_roles_for_reports():
    for report in ['Delayed Tasks Summary', 'Project wise Stock Tracking', 'Employee Hours Utilization Based On Timesheet']:
        if not frappe.db.get_value('Custom Role', dict(report=report)):
            frappe.get_doc(dict(
                doctype='Custom Role',
                report=report,
                roles=[
                    dict(role='Projects Manager'),
                    dict(role='Projects User')
                ]
            )).insert()
