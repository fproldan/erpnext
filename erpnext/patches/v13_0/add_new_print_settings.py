# Copyright (c) 2020, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

from erpnext.setup.install import create_sales_invoice_items_print_format_field


def execute():
    create_sales_invoice_items_print_format_field()
    frappe.db.commit()
