# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import cstr


def execute(filters=None):
    return get_columns(), get_sales_payment_data(filters)


def get_columns():
    return [
        _("Date") + ":Datetime:155",
        _("Owner") + ":Data:200",
        _("Payment Mode") + ":Data:150",
        _("Facturado") + ":Currency/currency:120",
        _("Payments") + ":Currency/currency:120",
        _("Referencia") + ":Data:120",
    ]


def get_sales_payment_data(filters):
    data = []
    sales_invoice_data = get_sales_invoice_data(filters)
    mode_of_payments = get_mode_of_payments(filters)
    mode_of_payment_details = get_mode_of_payment_details(filters)

    for inv in sales_invoice_data:
        owner_posting_date = inv["owner"] + cstr(inv["creation"])
        total_payment = 0
        for mop_detail in mode_of_payment_details.get(owner_posting_date, []):
            total_payment = total_payment + mop_detail[1]
        row = [inv.creation, inv.owner, ", ".join(mode_of_payments.get(owner_posting_date, [])), inv.grand_total, total_payment, '']
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
    return conditions


def get_sales_invoice_data(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql("""
        SELECT
            a.creation, a.owner,
            sum(a.grand_total) AS "grand_total",
            sum(a.base_paid_amount) AS "paid_amount",
            sum(a.outstanding_amount) AS "outstanding_amount"
        FROM `tabSales Invoice` a
        WHERE a.docstatus = 1
        AND {conditions}
        GROUP BY a.owner, a.creation
    """.format(conditions=conditions), filters, as_dict=1)


def get_mode_of_payments(filters):
    mode_of_payments = {}
    invoice_list = get_invoices(filters)
    invoice_list_names = ",".join('"' + invoice['name'] + '"' for invoice in invoice_list)
    if invoice_list:
        inv_mop = frappe.db.sql("""
            SELECT a.owner,a.creation, ifnull(b.mode_of_payment, '') AS mode_of_payment
            FROM `tabSales Invoice` a, `tabPayment Entry` b,`tabPayment Entry Reference` c
            WHERE a.name = c.reference_name
            AND b.name = c.parent
            AND b.docstatus = 1
            AND a.name IN ({invoice_list_names})
            UNION
            SELECT a.owner, a.creation, ifnull(a.voucher_type,'') AS mode_of_payment
            FROM `tabJournal Entry` a, `tabJournal Entry Account` b
            WHERE a.name = b.parent
            AND a.docstatus = 1
            AND b.reference_type = "Sales Invoice"
            AND b.reference_name IN ({invoice_list_names})
            """.format(invoice_list_names=invoice_list_names), as_dict=1)
        for d in inv_mop:
            mode_of_payments.setdefault(d["owner"] + cstr(d["creation"]), []).append(d.mode_of_payment)

    return mode_of_payments


def get_invoices(filters):
    return frappe.db.sql("""
        SELECT a.name
        FROM `tabSales Invoice` a
        WHERE a.docstatus = 1
        AND {conditions}
    """.format(conditions=get_conditions(filters)), filters, as_dict=1)


def get_mode_of_payment_details(filters):
    mode_of_payment_details = {}
    invoice_list = get_invoices(filters)
    invoice_list_names = ",".join('"' + invoice['name'] + '"' for invoice in invoice_list)
    if invoice_list:
        inv_mop_detail = frappe.db.sql("""
            SELECT a.owner,a.creation, ifnull(b.mode_of_payment, '') AS mode_of_payment, sum(b.base_paid_amount) AS paid_amount
            FROM `tabSales Invoice` a, `tabPayment Entry` b,`tabPayment Entry Reference` c
            WHERE a.name = c.reference_name
            AND b.name = c.parent
            AND b.docstatus = 1
            AND a.name IN ({invoice_list_names})
            GROUP BY a.owner, a.creation, mode_of_payment
            UNION
            SELECT a.owner, a.creation, ifnull(a.voucher_type,'') AS mode_of_payment, sum(b.credit)
            FROM `tabJournal Entry` a, `tabJournal Entry Account` b
            WHERE a.name = b.parent
            AND a.docstatus = 1
            AND b.reference_type = "Sales Invoice"
            AND b.reference_name IN ({invoice_list_names})
            GROUP BY a.owner, a.creation, mode_of_payment
            """.format(invoice_list_names=invoice_list_names), as_dict=1)

        for d in inv_mop_detail:
            mode_of_payment_details.setdefault(d["owner"] + cstr(d["creation"]), []).append((d.mode_of_payment, d.paid_amount))
    return mode_of_payment_details
