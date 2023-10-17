# Copyright(c) 2020, Frappe Technologies Pvt.Ltd.and Contributors
# License: GNU General Public License v3.See license.txt
import frappe
from frappe.utils import flt
from erpnext.accounts.utils import get_account_currency


def add_values_in_transaction_currency():
    for gl_entry in frappe.get_all('GL Entry', pluck='name'):
        gl_entry = frappe.get_doc('GL Entry', gl_entry)
        if not frappe.db.exists(gl_entry.voucher_type, gl_entry.voucher_no):
            continue
        doc = frappe.get_doc(gl_entry.voucher_type, gl_entry.voucher_no)
        account_currency = get_account_currency(gl_entry.account)
        data = {
            "transaction_currency": doc.get("currency") or doc.company_currency,
            "transaction_exchange_rate": doc.get("conversion_rate", 1),
            "debit_in_transaction_currency": get_value_in_transaction_currency(doc, gl_entry, account_currency, "debit"),
            "credit_in_transaction_currency": get_value_in_transaction_currency(doc, gl_entry, account_currency, "credit"),
		}
        for key, value in data.items():
            frappe.db.set_value('GL Entry', gl_entry.name, key, value)
        frappe.db.commit()


def get_value_in_transaction_currency(doc, gl_entry, account_currency, field):
    if account_currency == doc.get("currency"):
        return gl_entry.get(field + "_in_account_currency")
    else:
        return flt(gl_entry.get(field, 0) / doc.get("conversion_rate", 1))