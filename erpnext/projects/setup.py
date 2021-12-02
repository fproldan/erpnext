from __future__ import unicode_literals

import frappe


def setup_projects():
    add_custom_roles_for_reports()
    add_dashboard()


def remove_dashboard():
    frappe.db.delete("Dashboard", {"module": 'Projects'})
    frappe.db.delete("Number Card", {"module": 'Projects'})
    frappe.db.delete("Dashboard Chart", {"module": 'Projects'})
    frappe.db.delete("Dashboard Chart Link", {"parent": ('in', ('Project', 'Proyecto'))})
    frappe.db.delete("Number Card Link", {"parent": ('in', ('Project', 'Proyecto'))})
    frappe.db.commit()


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


def add_dashboard():
    remove_dashboard()

    dashboard_charts_and_number_cards = [{
        "chart_name": "Resumen del proyecto",
        "chart_type": "Report",
        "custom_options": "{\"type\": \"bar\", \"colors\": [\"#fc4f51\", \"#78d6ff\", \"#7575ff\"], \"axisOptions\": { \"shortenYAxisNumbers\": 1}, \"barOptions\": { \"stacked\": 1 }}",
        "docstatus": 0,
        "doctype": "Dashboard Chart",
        "dynamic_filters_json": "{\"company\":\"frappe.defaults.get_user_default(\\\"Company\\\")\"}",
        "filters_json": "{\"status\":\"Open\"}",
        "idx": 0,
        "is_public": 1,
        "is_standard": 0,
        "module": "Projects",
        "name": "Resumen del proyecto",
        "number_of_groups": 0,
        "owner": "Administrator",
        "report_name": "Project Summary",
        "timeseries": 0,
        "type": "Bar",
        "use_report_chart": 1,
        "y_axis": []
    }]

    dashboard = {
        "cards": [],
        "charts": [
            {
                "chart": "Resumen del proyecto",
                "width": "Full"
            }
        ],
        "dashboard_name": "Proyecto",
        "docstatus": 0,
        "doctype": "Dashboard",
        "idx": 0,
        "is_default": 0,
        "is_standard": 0,
        "module": "Projects",
        "name": "Proyecto",
        "owner": "Administrator"
    }

    for widget in dashboard_charts_and_number_cards:
        doc = frappe.new_doc(widget['doctype'])
        doc.update(widget)
        try:
            doc.insert()
        except Exception:
            continue

    doc = frappe.new_doc(dashboard['doctype'])
    doc.update(dashboard)
    doc.insert()

    frappe.db.commit()
