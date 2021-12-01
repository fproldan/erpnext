from __future__ import unicode_literals

import frappe


def setup_crm():
    add_dashboard()


def add_dashboard():
    frappe.db.delete("Dashboard", {"module": 'CRM'})
    frappe.db.delete("Number Card", {"module": 'CRM'})
    frappe.db.delete("Dashboard Chart", {"module": 'CRM'})
    frappe.db.delete("Dashboard Chart Link", {"parent": 'CRM'})
    frappe.db.delete("Number Card Link", {"parent": 'CRM'})
    frappe.db.commit()

    dashboard_charts_and_number_cards = [
        {
            "based_on": "creation",
            "chart_name": "Iniciativas",
            "chart_type": "Count",
            "custom_options": "{\"type\": \"line\", \"axisOptions\": {\"shortenYAxisNumbers\": 1}, \"tooltipOptions\": {}, \"lineOptions\": {\"regionFill\": 1}}",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "document_type": "Lead",
            "dynamic_filters_json": "[[\"Lead\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[]",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "last_synced_on": "2020-07-22 15:49:19.896501",
            "module": "CRM",
            "name": "Iniciativas",
            "number_of_groups": 0,
            "owner": "Administrator",
            "time_interval": "Weekly",
            "timeseries": 1,
            "timespan": "Last Quarter",
            "type": "Bar",
            "use_report_chart": 0,
            "y_axis": []
        },
        {
            "chart_name": "Fuente de la Iniciativa",
            "chart_type": "Group By",
            "custom_options": "{\"truncateLegends\": 1, \"maxSlices\": 8}",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "document_type": "Lead",
            "dynamic_filters_json": "[[\"Lead\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[]",
            "group_by_based_on": "source",
            "group_by_type": "Count",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "last_synced_on": "2020-07-22 16:11:14.170636",
            "module": "CRM",
            "name": "Fuente de la Iniciativa",
            "number_of_groups": 0,
            "owner": "Administrator",
            "timeseries": 0,
            "type": "Donut",
            "use_report_chart": 0,
            "y_axis": []
        },
        {
            "chart_name": "Oportunidades por Campaña",
            "chart_type": "Group By",
            "custom_options": "{\"truncateLegends\": 1, \"maxSlices\": 8}",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "document_type": "Opportunity",
            "dynamic_filters_json": "[[\"Opportunity\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[]",
            "group_by_based_on": "campaign",
            "group_by_type": "Count",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "last_synced_on": "2020-07-22 15:45:32.572011",
            "module": "CRM",
            "name": "Oportunidades por Campaña",
            "number_of_groups": 0,
            "owner": "Administrator",
            "timeseries": 0,
            "type": "Pie",
            "use_report_chart": 0,
            "y_axis": []
        },
        {
            "based_on": "creation",
            "chart_name": "Oportunidades",
            "chart_type": "Count",
            "custom_options": "",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "document_type": "Opportunity",
            "dynamic_filters_json": "[[\"Opportunity\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[]",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "last_synced_on": "2020-07-22 15:45:32.590967",
            "module": "CRM",
            "name": "Oportunidades",
            "number_of_groups": 0,
            "owner": "Administrator",
            "time_interval": "Weekly",
            "timeseries": 1,
            "timespan": "Last Quarter",
            "type": "Bar",
            "use_report_chart": 0,
            "y_axis": []
        },
        {
            "chart_name": "Oportunidades del Territorio",
            "chart_type": "Group By",
            "custom_options": "{\"truncateLegends\": 1, \"maxSlices\": 8}",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "document_type": "Opportunity",
            "dynamic_filters_json": "[[\"Opportunity\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[]",
            "group_by_based_on": "territory",
            "group_by_type": "Count",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "last_synced_on": "2020-07-22 15:45:32.134026",
            "module": "CRM",
            "name": "Oportunidades del Territorio",
            "number_of_groups": 0,
            "owner": "Administrator",
            "timeseries": 0,
            "type": "Donut",
            "use_report_chart": 0,
            "y_axis": []
        },
        {
            "aggregate_function_based_on": "opportunity_amount",
            "chart_name": "Ventas por territorio",
            "chart_type": "Group By",
            "custom_options": "",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "document_type": "Opportunity",
            "dynamic_filters_json": "[[\"Opportunity\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[[\"Opportunity\",\"status\",\"=\",\"Converted\",false]]",
            "group_by_based_on": "territory",
            "group_by_type": "Sum",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "last_synced_on": "2020-07-22 15:45:32.501313",
            "module": "CRM",
            "name": "Ventas por territorio",
            "number_of_groups": 0,
            "owner": "Administrator",
            "timeseries": 0,
            "type": "Bar",
            "use_report_chart": 0,
            "y_axis": []
        },
        {
            "based_on": "modified",
            "chart_name": "Oportunidades Ganadas",
            "chart_type": "Count",
            "docstatus": 0,
            "doctype": "Dashboard Chart",
            "document_type": "Opportunity",
            "dynamic_filters_json": "[[\"Opportunity\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[[\"Opportunity\",\"status\",\"=\",\"Converted\",false]]",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "last_synced_on": "2020-07-22 15:45:32.575964",
            "module": "CRM",
            "name": "Oportunidades Ganadas",
            "number_of_groups": 0,
            "owner": "Administrator",
            "time_interval": "Monthly",
            "timeseries": 1,
            "timespan": "Last Year",
            "type": "Bar",
            "use_report_chart": 0,
            "y_axis": []
        },
        {
            "docstatus": 0,
            "doctype": "Number Card",
            "document_type": "Lead",
            "dynamic_filters_json": "[[\"Lead\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[[\"Lead\",\"creation\",\"Timespan\",\"last month\",false]]",
            "function": "Count",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "label": "Iniciativas de los últimos 30 días",
            "module": "CRM",
            "name": "Iniciativas de los últimos 30 días",
            "owner": "Administrator",
            "show_percentage_stats": 1,
            "stats_time_interval": "Daily",
            "type": "Document Type"
        },
        {
            "docstatus": 0,
            "doctype": "Number Card",
            "document_type": "Opportunity",
            "dynamic_filters_json": "[[\"Opportunity\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[[\"Opportunity\",\"creation\",\"Timespan\",\"last month\",false]]",
            "function": "Count",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "label": "Oportunidades de los últimos 30 días",
            "module": "CRM",
            "name": "Oportunidades de los últimos 30 días",
            "owner": "Administrator",
            "show_percentage_stats": 1,
            "stats_time_interval": "Daily",
            "type": "Document Type"
        },
        {
            "docstatus": 0,
            "doctype": "Number Card",
            "document_type": "Opportunity",
            "dynamic_filters_json": "[[\"Opportunity\",\"status\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[[\"Opportunity\",\"company\",\"=\",null,false]]",
            "function": "Count",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "label": "Oportunidades Abiertas",
            "module": "CRM",
            "name": "Oportunidades Abiertas",
            "owner": "Administrator",
            "show_percentage_stats": 1,
            "stats_time_interval": "Daily",
            "type": "Document Type"
        },
        {
            "docstatus": 0,
            "doctype": "Number Card",
            "document_type": "Opportunity",
            "dynamic_filters_json": "[[\"Opportunity\",\"company\",\"=\",\"frappe.defaults.get_user_default(\\\"Company\\\")\"]]",
            "filters_json": "[[\"Opportunity\",\"creation\",\"Timespan\",\"last month\",false]]",
            "function": "Count",
            "idx": 0,
            "is_public": 1,
            "is_standard": 0,
            "label": "Oportunidades ganadas de los últimos 30 días",
            "module": "CRM",
            "name": "Oportunidades ganadas de los últimos 30 días",
            "owner": "Administrator",
            "show_percentage_stats": 1,
            "stats_time_interval": "Daily",
            "type": "Document Type"
        }
    ]

    dashboard = {
        "cards": [
            {"card": "Iniciativas de los últimos 30 días"},
            {"card": "Oportunidades de los últimos 30 días"},
            {"card": "Oportunidades ganadas de los últimos 30 días"},
            {"card": "Oportunidades Abiertas"}
        ],
        "charts": [
            {
                "chart": "Iniciativas",
                "width": "Full"
            },
            {
                "chart": "Oportunidades",
                "width": "Full"
            },
            {
                "chart": "Oportunidades Ganadas",
                "width": "Full"
            },
            {
                "chart": "Oportunidades del Territorio",
                "width": "Half"
            },
            {
                "chart": "Oportunidades por Campaña",
                "width": "Half"
            },
            {
                "chart": "Ventas por territorio",
                "width": "Full"
            },
            {
                "chart": "Fuente de la Iniciativa",
                "width": "Half"
            }
        ],
        "dashboard_name": "CRM",
        "docstatus": 0,
        "doctype": "Dashboard",
        "idx": 0,
        "is_default": 0,
        "is_standard": 0,
        "module": "CRM",
        "name": "CRM",
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
