# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.utils import flt
from six.moves import reduce

from erpnext.controllers.status_updater import StatusUpdater


class BankTransaction(StatusUpdater):
	def after_insert(self):
		self.unallocated_amount = abs(flt(self.withdrawal) - flt(self.deposit))

	def on_submit(self):
		self.clear_linked_payment_entries()
		self.set_status()

	def on_update_after_submit(self):
		self.update_allocations()
		self.clear_linked_payment_entries()
		self.set_status(update=True)

	def on_cancel(self):
		self.clear_linked_payment_entries(for_cancel=True)
		self.set_status(update=True)

	def update_allocations(self):
		if self.payment_entries:
			allocated_amount = reduce(lambda x, y: flt(x) + flt(y), [x.allocated_amount for x in self.payment_entries])
		else:
			allocated_amount = 0

		if allocated_amount:
			frappe.db.set_value(self.doctype, self.name, "allocated_amount", flt(allocated_amount))
			frappe.db.set_value(self.doctype, self.name, "unallocated_amount", abs(flt(self.withdrawal) - flt(self.deposit)) - flt(allocated_amount))

		else:
			frappe.db.set_value(self.doctype, self.name, "allocated_amount", 0)
			frappe.db.set_value(self.doctype, self.name, "unallocated_amount", abs(flt(self.withdrawal) - flt(self.deposit)))

		amount = self.deposit or self.withdrawal
		if amount == self.allocated_amount:
			frappe.db.set_value(self.doctype, self.name, "status", "Reconciled")

		self.reload()

	def clear_linked_payment_entries(self, for_cancel=False):
		for payment_entry in self.payment_entries:
			if payment_entry.payment_document in ["Payment Entry", "Journal Entry", "Purchase Invoice", "Expense Claim"]:
				self.clear_simple_entry(payment_entry, for_cancel=for_cancel)

			elif payment_entry.payment_document == "Sales Invoice":
				self.clear_sales_invoice(payment_entry, for_cancel=for_cancel)

	def clear_simple_entry(self, payment_entry, for_cancel=False):
		if payment_entry.payment_document == "Payment Entry":
			if frappe.db.get_value("Payment Entry", payment_entry.payment_entry, "payment_type") == "Internal Transfer":
				if len(get_reconciled_bank_transactions(payment_entry)) < 2:
					return

		clearance_date = self.date if not for_cancel else None

		gl_entry = frappe.db.get_value("GL Entry", dict(voucher_type=payment_entry.payment_document, voucher_no=payment_entry.payment_entry), ['credit', 'debit'], as_dict=1)
		gl_amount = gl_entry.credit if gl_entry.credit > 0 else gl_entry.debit

		if self.get_reconcilied_amount(payment_entry.payment_document, payment_entry.payment_entry) >= gl_amount:
			frappe.db.set_value(payment_entry.payment_document, payment_entry.payment_entry, "clearance_date", clearance_date)

	def clear_sales_invoice(self, payment_entry, for_cancel=False):
		clearance_date = self.date if not for_cancel else None
		frappe.db.set_value(
			"Sales Invoice Payment",
			dict(
				parenttype=payment_entry.payment_document,
				parent=payment_entry.payment_entry
			),
			"clearance_date", clearance_date)

	def get_reconcilied_amount(self, payment_document, payment_entry):
		if self.withdrawal > 0:
			select = "sum(bt.withdrawal) as sum"
		else:
			select = "sum(bt.deposit) as sum"

		amount = frappe.db.sql(f"""
		select {select}
		from `tabBank Transaction` as bt, `tabBank Transaction Payments` as btp
		where bt.name = btp.parent
		and btp.payment_entry = '{payment_entry}'
		and btp.payment_document = '{payment_document}'
		group by btp.payment_entry
		""", as_dict=1)

		if not len(amount):
			return 0
		return amount[0]['sum']

def get_reconciled_bank_transactions(payment_entry):
	reconciled_bank_transactions = frappe.get_all(
		'Bank Transaction Payments',
		filters = {
			'payment_entry': payment_entry.payment_entry
		},
		fields = ['parent']
	)

	return reconciled_bank_transactions

def get_total_allocated_amount(payment_entry):
	return frappe.db.sql("""
		SELECT
			SUM(btp.allocated_amount) as allocated_amount,
			bt.name
		FROM
			`tabBank Transaction Payments` as btp
		LEFT JOIN
			`tabBank Transaction` bt ON bt.name=btp.parent
		WHERE
			btp.payment_document = %s
		AND
			btp.payment_entry = %s
		AND
			bt.docstatus = 1""", (payment_entry.payment_document, payment_entry.payment_entry), as_dict=True)

def get_paid_amount(payment_entry, currency, bank_account):
	if payment_entry.payment_document in ["Payment Entry", "Sales Invoice", "Purchase Invoice"]:

		paid_amount_field = "paid_amount"
		if payment_entry.payment_document == 'Payment Entry':
			doc = frappe.get_doc("Payment Entry", payment_entry.payment_entry)
			paid_amount_field = ("base_paid_amount"
				if doc.paid_to_account_currency == currency else "paid_amount")

		return frappe.db.get_value(payment_entry.payment_document,
			payment_entry.payment_entry, paid_amount_field)

	elif payment_entry.payment_document == "Journal Entry":
		return frappe.db.get_value('Journal Entry Account', {'parent': payment_entry.payment_entry, 'account': bank_account}, "sum(credit_in_account_currency)")

	elif payment_entry.payment_document == "Expense Claim":
		return frappe.db.get_value(payment_entry.payment_document, payment_entry.payment_entry, "total_amount_reimbursed")

	else:
		frappe.throw("Please reconcile {0}: {1} manually".format(payment_entry.payment_document, payment_entry.payment_entry))

@frappe.whitelist()
def unclear_reference_payment(doctype, docname):
	if frappe.db.exists(doctype, docname):
		doc = frappe.get_doc(doctype, docname)
		if doctype == "Sales Invoice":
			frappe.db.set_value("Sales Invoice Payment", dict(parenttype=doc.payment_document,
				parent=doc.payment_entry), "clearance_date", None)
		else:
			frappe.db.set_value(doc.payment_document, doc.payment_entry, "clearance_date", None)

		return doc.payment_entry
