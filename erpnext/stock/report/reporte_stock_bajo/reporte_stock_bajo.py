# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)

	if not data:
		return [], [], None


	return columns, data, None

def get_conditions(filters):
	conditions = ""
	
	if filters.get('group_by_item'):
		if filters.get("company"):
			conditions += "AND company = %(company)s"
		if filters.get("item"):
			conditions += "AND item.name = %(item)s"
		if filters.get("item_group"):
			conditions += "AND item.item_group = %(item_group)s"
	else:
		if filters.get("warehouse"):
			conditions += "AND warehouse in %(warehouse)s"
		if filters.get("company"):
			conditions += "AND company = %(company)s"
		if filters.get("item"):
			conditions += "AND item.name = %(item)s"
		if filters.get("item_group"):
			conditions += "AND item.item_group = %(item_group)s"
		if filters.get("only_shortage"):
			conditions += "HAVING bin.actual_qty - item.safety_stock < 1"
	return conditions

def get_data(conditions, filters):

	if filters.get('group_by_item'):
		having = ""
		if filters.get("only_shortage"):
			having += "HAVING SUM(bin.actual_qty) - item.safety_stock < 1"
			
		data = frappe.db.sql("""
			SELECT
				"Todos los Almacenes" AS warehouse,
				bin.item_code,
				SUM(bin.actual_qty) AS actual_qty,
				item.safety_stock AS safety_stock,
				SUM(bin.actual_qty) - item.safety_stock AS low_stock,
				item.item_name
			FROM
				`tabBin` bin,
				`tabWarehouse` warehouse,
				`tabItem` item
			WHERE
				item.safety_stock > 0
				AND warehouse.name = bin.warehouse
				AND bin.item_code = item.name
				{0}
			GROUP BY item.item_name
			{1}
			ORDER BY item.safety_stock;""".format(conditions, having), filters, as_dict=1)
	else:
		data = frappe.db.sql("""
			SELECT
				bin.warehouse,
				bin.item_code,
				bin.actual_qty,
				item.safety_stock,
				bin.actual_qty - item.safety_stock AS low_stock,
				item.item_name
			FROM
				`tabBin` bin,
				`tabWarehouse` warehouse,
				`tabItem` item
			WHERE
				item.safety_stock > 0
				AND warehouse.name = bin.warehouse
				AND bin.item_code = item.name
				{0}
			ORDER BY item.safety_stock, item.item_code;""".format(conditions), filters, as_dict=1)

	return data

def get_columns():
	columns = [
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 250
		},
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 500
		},
		{
			"label": _("Cantidad"),
			"fieldname": "actual_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "qty"
		},
		{
			"label": _("Stock de Seguridad"),
			"fieldname": "safety_stock",
			"fieldtype": "Float",
			"width": 150,
			"convertible": "qty"
		},
		{
			"label": _("Stock Bajo"),
			"fieldname": "low_stock",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "qty"
		},
	]

	return columns
