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
        return frappe.render_template("erpnext/accounts/doctype/pos_closing_entry/closing_voucher_details.html", {"data": self, "currency": currency})

    def update_opening_entry(self, for_cancel=False):
        apertura_de_caja = frappe.get_doc("Apertura de Caja", self.apertura_de_caja)
        apertura_de_caja.cierre_de_caja = self.name if not for_cancel else None
        apertura_de_caja.set_status()
        apertura_de_caja.save()


def get_payment_entries(cierre_de_caja):
    for payment_reconciliation in cierre_de_caja.payment_reconciliation:
        payment_entries = frappe.db.get_all("Payment Entry", filters=[['creation', '>=', cierre_de_caja.period_start_date], ['creation', '<=', cierre_de_caja.period_end_date], ['mode_of_payment', '=', payment_reconciliation.mode_of_payment]], fields=["total_allocated_amount"])
        total_allocated_amount = 0
        if payment_entries:
            total_allocated_amount = [pe.get("total_allocated_amount", 0) for pe in payment_entries][0]

        print(total_allocated_amount)


def make_closing_entry_from_opening(opening_entry):
    closing_entry = frappe.new_doc("Cierre de Caja")
    closing_entry.pos_opening_entry = opening_entry.name
    closing_entry.period_start_date = opening_entry.period_start_date
    closing_entry.period_end_date = frappe.utils.get_datetime()
    closing_entry.user = opening_entry.user
    closing_entry.company = opening_entry.company
    closing_entry.grand_total = 0
    closing_entry.net_total = 0
    closing_entry.total_quantity = 0

    payments = []
    for detail in opening_entry.balance_details:
        payments.append(frappe._dict({
            'mode_of_payment': detail.mode_of_payment,
            'opening_amount': detail.opening_amount,
            'expected_amount': detail.opening_amount
        }))

    closing_entry.set("payment_reconciliation", payments)
    return closing_entry
