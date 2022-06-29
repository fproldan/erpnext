# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    filtros = ""

    if 'supplier' in filters:
        filtros += """ AND supplier = "{supplier}" """.format(supplier=filters.get("supplier"))

    if 'schedule_date' in filters:
        filtros += """ AND schedule_date = "{schedule_date}" """.format(schedule_date=filters.get('schedule_date'))

    if 'reclamado' in filters:
        filtros += """ AND reclamado = "{reclamado}" """.format(reclamado=filters.get('reclamado'))

    query = """
        SELECT supplier, name, IF(per_received > 0, "Parcial", "Completo") AS per_received, schedule_date, reclamado, nuevo_pacto_entrega
        FROM `tabPurchase Order`
        WHERE docstatus = 1
        AND DATEDIFF(CURDATE(), schedule_date) >= 7
        AND per_received < 100
        {filtros}
        ORDER BY DATEDIFF(CURDATE(), schedule_date) DESC
    """.format(filtros=filtros)

    data = frappe.db.sql(query, as_dict=1)
    return get_columns(), data


def get_columns():
    return [
        {
            "fieldname": "supplier",
            "label": "Proveedor",
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 160
        },
        {
            "fieldname": "name",
            "label": "Órden de Compra",
            "fieldtype": "Link",
            "options": "Purchase Order",
            "width": 200
        },
        {
            "fieldname": "per_received",
            "label": "Pediente de Entrega",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname": "schedule_date",
            "label": "Fecha de Entrega",
            "fieldtype": "Date",
            "width": 200
        },
        {
            "fieldname": "reclamado",
            "label": "Fecha de Reclamo",
            "fieldtype": "Date",
            "width": 180
        },
        {
            "fieldname": "nuevo_pacto_entrega",
            "label": "Fecha de Nuevo Pacto de Entrega",
            "fieldtype": "Date",
            "width": 250
        },
    ]
