# Copyright (c) 2022, Diamo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    """
    Item    Valid From  Price List  Price
    Item 1  2020-01-01  L1          100
    Item 1  2020-02-02  L2          200
    Item 2  2020-01-01  L2          50
    Item 3  2020-01-01  L1          500
    Item 3  2020-01-10  L1          700
    Item 3  2019-10-10  L3          750
    Item 1  L1  100
    Item 1  L2  200
    Item 2  L2  50
    Item 3  L1  700
    Item 3  L3  750
    """
    if filters.historico and not filters.item:
        frappe.throw("Debe seleccionar un producto para obtener el histórico")

    item_filter = ''
    price_list_filter = ''
    item_group_filter = ''
    brand_filter = ''
    al_dia_filter = ''
    filters_formatted = ''

    if filters.item:
        item_filter = " AND t2.item_code='{}'".format(filters.item)

    if filters.price_list:
        price_list_filter = " AND t2.price_list='{}'".format(filters.price_list)

    if filters.brand:
        brand_filter = " AND t2.brand='{}'".format(filters.brand)

    if filters.al_dia:
        al_dia_filter = " AND t2.valid_from <= curdate()"

    if item_filter or price_list_filter or item_group_filter or brand_filter or al_dia_filter:
        filters_formatted = ' {} {} {} {} {}'.format(item_filter, price_list_filter, item_group_filter, brand_filter, al_dia_filter)

    if filters.historico:
        data = frappe.db.sql("""
            SELECT i.item_group, t2.item_code, i.brand, i.item_name, t2.uom, t2.currency, t2.price_list, t2.price_list_rate
            FROM `tabItem Price` t2
            JOIN `tabItem` i ON t2.item_code = i.item_code
            WHERE True
            {filters}
            ORDER BY t2.price_list DESC, t2.valid_from DESC;
        """.format(filters=filters_formatted), as_dict=1)
    else:
        inner_filter = ''
        if filters.al_dia:
            inner_filter = ' AND valid_from <= curdate()'

        data = frappe.db.sql("""
            SELECT i.item_group, t2.item_code, i.brand, i.item_name, t2.uom, t2.currency, t2.price_list, t2.price_list_rate
            FROM
            (
              SELECT item_code, price_list, max(valid_from) AS valid_from, price_list_rate
              FROM `tabItem Price`
              WHERE ifnull(valid_upto , curdate()) >= curdate()
              {inner_filter}
              GROUP BY item_code, price_list
            ) t1
            INNER JOIN `tabItem Price` t2 ON t2.item_code = t1.item_code AND t2.valid_from = t1.valid_from AND t2.price_list=t1.price_list
            JOIN `tabItem` i ON t2.item_code = i.item_code
            WHERE True
            {filters}
            GROUP BY t2.item_code, t2.price_list
            ORDER BY t2.item_code, t2.uom DESC, t2.valid_from DESC;
        """.format(filters=filters_formatted, inner_filter=inner_filter), as_dict=1)

    for d in data:
        item_purchase_user = frappe.db.get_value("Item Default", {"parent": d['item_code'], "company": filters.company}, 'purchase_user')
        item_group_purchase_user = frappe.db.get_value("Item Default", {"parent": d['item_group'], "company": filters.company}, 'purchase_user')
        purchase_user = item_purchase_user or item_group_purchase_user
        d.update({"purchase_user": purchase_user})

    if filters.get('purchase_user'):
        data = [d for d in data if d['purchase_user'] == filters.get('purchase_user')]
    return get_columns(), data


def get_columns():
    return [
   		{
            "fieldname": "item_group",
            "label": "Grupo de producto",
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 180
        },
        {
            "fieldname": "item_code",
            "label": "Codigo",
            "fieldtype": "Link",
            "options": "Item",
            "width": 180
        },
        {
            "fieldname": "item_name",
            "label": "Nombre",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname": "price_list_rate",
            "label": "Precio",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "currency",
            "label": "Moneda",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "fieldname": "uom",
            "label": "Uom",
            "fieldtype": "Link",
            "options": "Uom",
            "width": 80
        },
        {
            "fieldname": "price_list",
            "label": "Lista de Precio",
            "fieldtype": "Link",
            "options": "Price List",
            "width": 200
        },
        {
            "fieldname": "brand",
            "label": "Marca",
            "fieldtype": "Link",
            "options": "Brand",
            "width": 150
        },
        {
            "fieldname": "purchase_user",
            "label": "Asignado a",
            "fieldtype": "Link",
            "options": "User",
            "width": 150
        }
    ]
