# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
    return get_columns(), get_sales_payment_data(filters)


def get_columns():
    return [
        _("Date") + ":Datetime:155",
        _("Owner") + ":Data:200",
        _("name") + ":Link/Payment Entry:200",
        _("Payment Mode") + ":Data:150",
        _("Payments") + ":Currency/currency:120",
        _("Referencia") + ":Data:250",
    ]


def get_sales_payment_data(filters):
    data = []
    for payment_entry in get_payment_entries(filters):
        row = [payment_entry.creation, payment_entry.owner, payment_entry.name, payment_entry.mode_of_payment, payment_entry.paid_amount, payment_entry.reference_no]
        data.append(row)
    return data


def get_conditions(filters):
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += " and a.creation >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and a.creation <= %(to_date)s"
    if filters.get("company"):
        conditions += " and a.company=%(company)s"
    if filters.get("owner"):
        conditions += " and a.owner = %(owner)s"
    if filters.get("mode_of_payment"):
        accounts = []
        for mode in filters.get("mode_of_payment"):
            accounts.append(frappe.db.get_value("Mode of Payment Account", {"parent": mode, "company": filters.get("company")}, "default_account"))

        filters["accounts"] = accounts
        conditions += " and a.mode_of_payment in %(mode_of_payment)s or a.paid_to in %(accounts)s or a.paid_from in %(accounts)s"
    return conditions


def get_payment_entries(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql("""
        SELECT a.name, a.creation, a.owner, a.paid_amount, a.reference_no, a.mode_of_payment, a.reference_no
        FROM `tabPayment Entry` a
        WHERE a.docstatus = 1
        AND {conditions}
        ORDER BY a.creation
    """.format(conditions=conditions), filters, as_dict=1)
