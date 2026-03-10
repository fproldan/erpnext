import frappe
from erpnext.buying.utils import update_last_purchase_rate


def execute():
    invoices = frappe.get_all("Purchase Invoice", {"docstatus": 1}, pluck="name")
    for invoice in invoices:
        doc = frappe.get_doc("Purchase Invoice", invoice)
        update_last_purchase_rate(doc, 1)

    frappe.db.commit()