import frappe
from erpnext.buying.utils import update_last_purchase_rate


def execute():
    for item in frappe.get_all("Item", pluck="name"):
        last_purchase_invoice = frappe.db.get_value(
            "Purchase Invoice Item",
            {"item_code": item},
            "parent",
            order_by="creation desc",
        )
        if last_purchase_invoice:
            doc = frappe.get_doc("Purchase Invoice", last_purchase_invoice)
            update_last_purchase_rate(doc, 1)
    frappe.db.commit()