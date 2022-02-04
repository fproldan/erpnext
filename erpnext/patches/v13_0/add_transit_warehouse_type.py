# Copyright(c) 2020, Frappe Technologies Pvt.Ltd.and Contributors
# License: GNU General Public License v3.See license.txt

from __future__ import unicode_literals

import frappe


def execute():
    frappe.reload_doc("stock", "doctype", "warehouse_type")
    if not frappe.db.exists('Warehouse Type', 'Tránsito'):
        doc = frappe.new_doc('Warehouse Type')
        doc.name = 'Tránsito'
        doc.insert()
