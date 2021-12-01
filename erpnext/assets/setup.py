from __future__ import unicode_literals

import frappe


def setup_assets():
    add_dashboard()


def add_dashboard():
    frappe.db.delete("Dashboard", {"module": 'Asset'})
    frappe.db.delete("Number Card", {"module": 'Asset'})
    frappe.db.delete("Dashboard Chart", {"module": 'Asset'})
    frappe.db.delete("Dashboard Chart Link", {"parent": ('in', ('Activos', 'Asset'))})
    frappe.db.delete("Number Card Link", {"parent": ('in', ('Activos', 'Asset'))})
    frappe.db.commit()

    dashboard_charts_and_number_cards = [
        {
            "chart_name": "Análisis de valor de activos",
            "chart_type": "Report",
            "custom_options": "{\"type\": \"bar\", \"barOptions\": {\"stacked\": 1}, \"axisOptions\": {\"shortenYAxisNumbers\": 1}, \"tooltipOptions\": {}}",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "dynamic_filters_json": "{\"company\":\"frappe.defaults.get_user_default(\\\"Company\\\")\",\"from_fiscal_year\":\"frappe.sys_defaults.fiscal_year\",\"to_fiscal_year\":\"frappe.sys_defaults.fiscal_year\",\"from_date\":\"frappe.datetime.add_months(frappe.datetime.nowdate(), -12)\",\"to_date\":\"frappe.datetime.nowdate()\"}",
            "filters_json": "{\"status\":\"In Location\",\"filter_based_on\":\"Fiscal Year\",\"period_start_date\":\"2020-04-01\",\"period_end_date\":\"2021-03-31\",\"date_based_on\":\"Purchase Date\",\"group_by\":\"--Select a group--\"}",
            "group_by_type": "Count",
            "idx": 0,
            "is_public": 0,
            "is_standard": 0,
            "module": "Assets",
            "name": "Análisis de valor de activos",
            "number_of_groups": 0,
            "owner": "Administrator",
            "report_name": "Fixed Asset Register",
            "time_interval": "Yearly",
            "timeseries": 0,
            "timespan": "Last Year",
            "type": "Bar",
            "use_report_chart": 1,
            "y_axis": []
        },
        {
            "chart_name": "Valor de los activos por categoría",
            "chart_type": "Report",
            "custom_options": "{\"type\": \"donut\", \"height\": 300, \"axisOptions\": {\"shortenYAxisNumbers\": 1}}",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "dynamic_filters_json": "{\"company\":\"frappe.defaults.get_user_default(\\\"Company\\\")\",\"from_date\":\"frappe.datetime.add_months(frappe.datetime.nowdate(), -12)\",\"to_date\":\"frappe.datetime.nowdate()\"}",
            "filters_json": "{\"status\":\"In Location\",\"group_by\":\"Asset Category\",\"is_existing_asset\":0}",
            "idx": 0,
            "is_public": 0,
            "is_standard": 0,
            "module": "Assets",
            "name": "Valor de los activos por categoría",
            "number_of_groups": 0,
            "owner": "Administrator",
            "report_name": "Fixed Asset Register",
            "timeseries": 0,
            "type": "Donut",
            "use_report_chart": 0,
            "x_field": "asset_category",
            "y_axis": [
                {
                    "y_field": "asset_value"
                }
            ]
        },
        {
            "chart_name": "Valor de los activos por ubicación",
            "chart_type": "Report",
            "custom_options": "{\"type\": \"donut\", \"height\": 300, \"axisOptions\": {\"shortenYAxisNumbers\": 1}}",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "dynamic_filters_json": "{\"company\":\"frappe.defaults.get_user_default(\\\"Company\\\")\",\"from_date\":\"frappe.datetime.add_months(frappe.datetime.nowdate(), -12)\",\"to_date\":\"frappe.datetime.nowdate()\"}",
            "filters_json": "{\"status\":\"In Location\",\"group_by\":\"Location\",\"is_existing_asset\":0}",
            "idx": 0,
            "is_public": 0,
            "is_standard": 0,
            "module": "Assets",
            "name": "Valor de los activos por ubicación",
            "number_of_groups": 0,
            "owner": "Administrator",
            "report_name": "Fixed Asset Register",
            "timeseries": 0,
            "type": "Donut",
            "use_report_chart": 0,
            "x_field": "location",
            "y_axis": [
                {
                    "y_field": "asset_value"
                }
            ]
        },
        {
            "aggregate_function_based_on": "value_after_depreciation",
            "docstatus": 0,
            "doctype": "Number Card",
            "document_type": "Asset",
            "filters_json": "[]",
            "function": "Sum",
            "idx": 0,
            "is_public": 0,
            "is_standard": 0,
            "label": "Valor del activo",
            "module": "Assets",
            "name": "Valor del activo",
            "owner": "Administrator",
            "show_percentage_stats": 1,
            "stats_time_interval": "Monthly",
            "type": "Document Type"
        },
        {
            "docstatus": 0,
            "doctype": "Number Card",
            "document_type": "Asset",
            "filters_json": "[[\"Asset\",\"creation\",\"Timespan\",\"this year\",false]]",
            "function": "Count",
            "idx": 0,
            "is_public": 0,
            "is_standard": 0,
            "label": "Nuevos activos (este año)",
            "module": "Assets",
            "name": "Nuevos activos (este año)",
            "owner": "Administrator",
            "show_percentage_stats": 1,
            "stats_time_interval": "Monthly",
            "type": "Document Type"
        },
        {
            "docstatus": 0,
            "doctype": "Number Card",
            "document_type": "Asset",
            "filters_json": "[]",
            "function": "Count",
            "idx": 0,
            "is_public": 0,
            "is_standard": 0,
            "label": "Activos totales",
            "module": "Assets",
            "name": "Activos totales",
            "owner": "Administrator",
            "show_percentage_stats": 1,
            "stats_time_interval": "Monthly",
            "type": "Document Type"
        }
    ]

    dashboard = {
        "cards": [
            {
                "card": "Activos totales"
            },
            {
                "card": "Nuevos activos (este año)"
            },
            {
                "card": "Valor del activo"
            }
        ],
        "charts": [
            {
                "chart": "Análisis de valor de activos",
                "width": "Full"
            },
            {
                "chart": "Valor de los activos por categoría",
                "width": "Half"
            },
            {
                "chart": "Valor de los activos por ubicación",
                "width": "Half"
            }
        ],
        "dashboard_name": "Activos",
        "docstatus": 0,
        "doctype": "Dashboard",
        "idx": 0,
        "is_default": 0,
        "is_standard": 0,
        "module": "Assets",
        "name": "Activos",
        "owner": "Administrator"
    }

    for widget in dashboard_charts_and_number_cards:
        doc = frappe.new_doc(widget['doctype'])
        doc.update(widget)
        doc.insert()

    doc = frappe.new_doc(dashboard['doctype'])
    doc.update(dashboard)
    doc.insert()

    frappe.db.commit()
