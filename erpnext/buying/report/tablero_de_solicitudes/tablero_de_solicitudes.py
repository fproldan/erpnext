# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}

    filter_company = ''
    filter_status = ''
    filter_material_request_type  = ''
    filter_name  = ''
    filter_title  = ''

    if filters.get('company'):
        filter_company = "AND mr.company='{}'".format(filters.get('company'))

    if filters.get("status"):
        status_map = {
            _("Draft"): "Draft",
            _("Submitted"): "Submitted",
            _("Stopped"): "Stopped",
            _("Cancelled"): "Cancelled",
            _("Pending"): "Pending",
            _("Partially Ordered"): "Partially Ordered",
            _("Partially Received"): "Partially Received",
            _("Ordered"): "Ordered",
            _("Issued"): "Issued",
            _("Transferred"): "Transferred",
            _("Received"): "Received",
        }
        filter_status += " AND mr.status='{}'".format(status_map.get(filters.get("status")))

    if filters.get("material_request_type"):
        material_request_type_map = {
            _("Purchase"): "Purchase",
            _("Material Transfer"): "Material Transfer",
            _("Material Issue"): "Material Issue",
        }
        filter_material_request_type += " AND mr.material_request_type='{}'".format(material_request_type_map.get(filters.get("material_request_type")))

    if filters.get('name'):
        filter_name = "AND mr.name LIKE '%{}%'".format(filters.get('name'))
    if filters.get('title'):
        filter_title = "AND mr.title LIKE '%{}%'".format(filters.get('title'))
    query = """
        SELECT mr.name, mr.title, mr.material_request_type, mr.status, mr.schedule_date, mr.company, mr.set_warehouse, mr.per_ordered, mr.per_received, mr.transfer_status
        FROM `tabMaterial Request` mr
        WHERE True
        {filter_company}
        {filter_status}
        {filter_material_request_type}
        {filter_name}
        {filter_title};
    """
    results = frappe.db.sql(query.format(filter_company=filter_company, filter_status=filter_status, filter_material_request_type=filter_material_request_type, filter_name=filter_name, filter_title=filter_title), as_dict=True)
    
    for r in results:
        r['status'] = _(r['status'])
        r['material_request_type'] = _(r['material_request_type'])
        
    return get_columns(), results


def get_columns():
    columns = [
        {
            "fieldname": "name",
            "label": ("Identificador"),
            "fieldtype": "Link",
            "options": "Material Request",
            "width": 200
        },
        {
            "fieldname": "title",
            "label": ("Nombre"),
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "material_request_type",
            "label": ("Propósito"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "status",
            "label": ("Estado"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "schedule_date",
            "label": ("Solicitado para"),
            "fieldtype": "Date",
            "width": 120
        },
        {
            "fieldname": "company",
            "label": ("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "width": 200
        },
        {
            "fieldname": "set_warehouse",
            "label": ("Almacén de destino"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 200
        },
        {
            "fieldname": "per_ordered",
            "label": ("% Ordenado"),
            "fieldtype": "Percent",
            "width": 110
        },
        {
            "fieldname": "per_received",
            "label": ("% Recibido"),
            "fieldtype": "Percent",
            "width": 110
        },
        {
            "fieldname": "transfer_status",
            "label": ("Estado de transferencia"),
            "fieldtype": "Data",
            "width": 200
        },
    ]
    return columns