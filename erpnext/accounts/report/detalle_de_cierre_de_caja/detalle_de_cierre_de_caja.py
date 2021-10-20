# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
    return get_columns(), get_sales_payment_data(filters)


def get_columns():
    return [
        {
            "fieldname": "date",
            "label": _("Date"),
            "fieldtype": "Datetime",
            "width": 155
        },
        {
            "fieldname": "owner",
            "label": _("Owner"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "name",
            "label": _("Name"),
            "fieldtype": "Link",
            "options": "Payment Entry",
            "width": 200
        },
        {
            "fieldname": "payment_mode",
            "label": _("Payment Mode"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "payments",
            "label": _("Payments"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "referencia",
            "label": _("Referencia"),
            "fieldtype": "Data",
            "width": 250
        },
    ]


def get_sales_payment_data(filters):
    data = []
    for payment_entry in get_payment_entries(filters):
        data.append({
            'date': payment_entry.creation,
            'owner': payment_entry.owner,
            'name': payment_entry.name,
            'payment_mode': payment_entry.mode_of_payment,
            'payments': payment_entry.paid_amount,
            'referencia': payment_entry.reference_no,
            'signo': payment_entry.signo,
        })
    return data


def get_conditions(filters):
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += " and a.creation >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and a.creation <= %(to_date)s"
    if filters.get("company"):
        conditions += " and a.company=%(company)s "
    mode_of_payment = filters.get("mode_of_payment", None) or [mp["name"] for mp in frappe.get_all("Mode of Payment", {"company": filters.get("company")}, "name")]
    filters["accounts"] = list(set([frappe.db.get_value("Mode of Payment Account", {"parent": mode, "company": filters.get("company")}, "default_account") for mode in mode_of_payment]))
    return conditions


def get_payment_entries(filters):
    conditions = get_conditions(filters)
    accounts = '({})'.format(', '.join(['"%s"' % x for x in filters.get("accounts")]))

    return frappe.db.sql("""
        SELECT *
        FROM
            (
                SELECT a.name, a.creation, a.owner, a.paid_amount, a.reference_no, a.mode_of_payment, 1 AS signo
                FROM `tabPayment Entry` a
                WHERE a.docstatus = 1
                AND {conditions}
                AND a.paid_to in {accounts}

                UNION

                SELECT a.name, a.creation, a.owner, a.paid_amount, a.reference_no, a.mode_of_payment, -1 AS signo
                FROM `tabPayment Entry` a
                WHERE a.docstatus = 1
                AND {conditions}
                AND a.paid_from in {accounts}
            ) results
        ORDER BY creation
    """.format(conditions=conditions, accounts=accounts), filters, as_dict=1)
