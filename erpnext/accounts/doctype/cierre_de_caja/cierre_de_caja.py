# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from erpnext.controllers.status_updater import StatusUpdater


class CierredeCaja(StatusUpdater):
    def validate(self):
        if frappe.db.get_value("Apertura de Caja", self.apertura_de_caja, "status") != "Open":
            frappe.throw("La Apertura de Caja seleccionada debe estar Abierta", title="Apertura de Caja inválida")

    @frappe.whitelist()
    def get_payment_reconciliation_details(self):
        currency = frappe.get_cached_value('Company', self.company, "default_currency")
        return frappe.render_template("erpnext/accounts/doctype/cierre_de_caja/cierre_de_caja_details.html", {"data": self, "currency": currency})

    @frappe.whitelist()
    def get_totals(self):
        totals = {}

        sales_invoices = frappe.db.get_all("Sales Invoice", filters=[['creation', '>=', self.period_start_date], ['creation', '<=', self.period_end_date], ['docstatus', '=', '1'], ['owner', '=', self.user]], fields=["grand_total"])
        totals["bill_total"] = sum(sales_invoice['grand_total'] for sales_invoice in sales_invoices)

        modes = []

        cash_cheque_modes = [mp["name"] for mp in frappe.get_all("Mode of Payment", filters=[["type", "in", ("Cash", "Cheque")]])]

        for payment_reconciliation in self.payment_reconciliation:
            if payment_reconciliation.mode_of_payment in cash_cheque_modes:
                modes.append(payment_reconciliation.mode_of_payment)

        filters = [['creation', '>=', self.period_start_date], ['creation', '<=', self.period_end_date], ['mode_of_payment', 'in', modes], ['docstatus', '=', '1'], ['owner', '=', self.user]]
        payment_entries = frappe.db.get_all("Payment Entry", filters=filters, fields=["total_allocated_amount"])
        total_cash_cheque = sum(payment_entry['total_allocated_amount'] for payment_entry in payment_entries)

        totals['total_cash_cheque'] = total_cash_cheque
        return totals

    def update_opening_entry(self, for_cancel=False):
        apertura_de_caja = frappe.get_doc("Apertura de Caja", self.apertura_de_caja)
        apertura_de_caja.cierre_de_caja = self.name if not for_cancel else None
        apertura_de_caja.set_status()
        apertura_de_caja.save()

    def on_submit(self):
        self.set_status(update=True, status='Submitted')
        self.update_opening_entry()

    def on_cancel(self):
        self.set_status(update=True, status='Cancelled')
        self.update_opening_entry(for_cancel=True)


def get_expected_amount(mode_of_payment, period_start_date, period_end_date, owner):
    filters = [['creation', '>=', period_start_date], ['creation', '<=', period_end_date], ['mode_of_payment', '=', mode_of_payment], ['docstatus', '=', '1'], ['owner', '=', owner]]
    payment_entries = frappe.db.get_all("Payment Entry", filters=filters, fields=["total_allocated_amount"])
    return sum(payment_entry['total_allocated_amount'] for payment_entry in payment_entries)


@frappe.whitelist()
def get_payment_reconciliation(apertura_de_caja, period_start_date, period_end_date):
    apertura_de_caja = frappe.get_doc("Apertura de Caja", apertura_de_caja)

    payment_reconciliations = []

    for balance_detail in apertura_de_caja.balance_details:
        payment_reconciliations.append({
            "mode_of_payment": balance_detail.mode_of_payment,
            "opening_amount": balance_detail.opening_amount,
            "expected_amount": balance_detail.opening_amount + get_expected_amount(balance_detail.mode_of_payment, period_start_date, period_end_date, apertura_de_caja.user)
        })

    return payment_reconciliations
