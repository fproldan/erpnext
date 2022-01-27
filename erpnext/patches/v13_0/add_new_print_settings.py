# Copyright (c) 2020, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

from erpnext.setup.install import create_print_sales_invoice_item_code_description, create_print_sales_invoice_item_name_description


def execute():
    create_print_sales_invoice_item_code_description()
    create_print_sales_invoice_item_name_description()
    frappe.db.commit()
