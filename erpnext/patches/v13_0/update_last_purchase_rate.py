import frappe
from frappe.utils import flt


def execute():
	for item in frappe.get_all("Item", pluck="name"):
		last_purchase_invoice = frappe.db.get_value(
			"Purchase Invoice Item",
			{"item_code": item},
			"name",
			order_by="creation desc",
		)
		last_purchase_rate = None
		if last_purchase_invoice:
			d = frappe.get_doc("Purchase Invoice Item", last_purchase_invoice)
			if flt(d.conversion_factor):
				last_purchase_rate = flt(d.base_net_rate) / flt(d.conversion_factor)
		
		frappe.db.set_value('Item', d.item_code, 'last_purchase_rate', flt(last_purchase_rate))                 
		frappe.db.commit()