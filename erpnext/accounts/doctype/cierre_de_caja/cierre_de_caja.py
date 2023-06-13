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

    def get_accounts(self, cash_cheque=False):
        if cash_cheque:
            cash_cheque_modes = [mp["name"] for mp in frappe.get_all("Mode of Payment", filters=[["type", "in", ("Cash", "Cheque")]])]
            modes = [payment_reconciliation.mode_of_payment for payment_reconciliation in self.payment_reconciliation if payment_reconciliation.mode_of_payment in cash_cheque_modes]
        else:
            modes = [payment_reconciliation.mode_of_payment for payment_reconciliation in self.payment_reconciliation]
        return [frappe.db.get_value("Mode of Payment Account", {"parent": mode_of_payment, "company": self.company}, "default_account") for mode_of_payment in modes]

    @frappe.whitelist()
    def get_totals(self):
        totals = {}

        sales_invoices = frappe.db.get_all("Sales Invoice", filters=[['creation', '>=', self.period_start_date], ['creation', '<=', self.period_end_date], ['docstatus', '=', '1'], ['owner', '=', self.user]], fields=["grand_total"])
        totals["bill_total"] = sum(sales_invoice['grand_total'] for sales_invoice in sales_invoices)

        accounts = self.get_accounts(True)
        positive_entries_filter = [['creation', '>=', self.period_start_date], ['creation', '<=', self.period_end_date], ['paid_to', 'in', accounts], ['docstatus', '=', '1']]
        negative_entries_filter = [['creation', '>=', self.period_start_date], ['creation', '<=', self.period_end_date], ['paid_from', 'in', accounts], ['docstatus', '=', '1']]
        positive_payment_entries = frappe.db.get_all("Payment Entry", filters=positive_entries_filter, fields=["paid_amount"])
        negative_payment_entries = frappe.db.get_all("Payment Entry", filters=negative_entries_filter, fields=["paid_amount"])
        total_cash_cheque = sum(payment_entry['paid_amount'] for payment_entry in positive_payment_entries) + sum(payment_entry['paid_amount'] * -1 for payment_entry in negative_payment_entries)
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


def get_expected_amount(mode_of_payment, period_start_date, period_end_date, owner, company):
    account = frappe.db.get_value("Mode of Payment Account", {"parent": mode_of_payment, "company": company}, "default_account")
    positive_entries_filter = [['creation', '>=', period_start_date], ['creation', '<=', period_end_date], ['paid_to', '=', account], ['docstatus', '=', '1']]
    negative_entries_filter = [['creation', '>=', period_start_date], ['creation', '<=', period_end_date], ['paid_from', '=', account], ['docstatus', '=', '1']]
    positive_payment_entries = frappe.db.get_all("Payment Entry", filters=positive_entries_filter, fields=["paid_amount"])
    negative_payment_entries = frappe.db.get_all("Payment Entry", filters=negative_entries_filter, fields=["paid_amount"])
    return sum(payment_entry['paid_amount'] for payment_entry in positive_payment_entries) + sum(payment_entry['paid_amount'] * -1 for payment_entry in negative_payment_entries)


@frappe.whitelist()
def get_payment_reconciliation(apertura_de_caja, period_start_date, period_end_date):
    apertura_de_caja = frappe.get_doc("Apertura de Caja", apertura_de_caja)

    payment_reconciliations = []

    for balance_detail in apertura_de_caja.balance_details:
        payment_reconciliations.append({
            "mode_of_payment": balance_detail.mode_of_payment,
            "opening_amount": balance_detail.opening_amount,
            "expected_amount": balance_detail.opening_amount + get_expected_amount(balance_detail.mode_of_payment, period_start_date, period_end_date, apertura_de_caja.user, apertura_de_caja.company)
        })

    return payment_reconciliations
