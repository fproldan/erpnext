# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form
from erpnext.stock.get_item_details import get_item_price


class ProductBundle(Document):
	def autoname(self):
		self.name = self.new_item_code

	def validate(self):
		self.validate_main_item()
		self.validate_child_items()
		from erpnext.utilities.transaction_base import validate_uom_is_integer
		validate_uom_is_integer(self, "uom", "qty")

	def on_trash(self):
		linked_doctypes = ["Delivery Note", "Sales Invoice", "POS Invoice", "Purchase Receipt", "Purchase Invoice",
			"Stock Entry", "Stock Reconciliation", "Sales Order", "Purchase Order", "Material Request"]

		invoice_links = []
		for doctype in linked_doctypes:
			item_doctype = doctype + " Item"

			if doctype == "Stock Entry":
				item_doctype = doctype + " Detail"

			invoices = frappe.db.get_all(item_doctype, {"item_code": self.new_item_code, "docstatus": 1}, ["parent"])

			for invoice in invoices:
				invoice_links.append(get_link_to_form(doctype, invoice['parent']))

		if len(invoice_links):
			frappe.throw(
				"This Product Bundle is linked with {0}. You will have to cancel these documents in order to delete this Product Bundle"
				.format(", ".join(invoice_links)), title=_("Not Allowed"))

	def validate_main_item(self):
		"""Validates, main Item is not a stock item"""
		if frappe.db.get_value("Item", self.new_item_code, "is_stock_item"):
			frappe.throw(_("Parent Item {0} must not be a Stock Item").format(self.new_item_code))

	def validate_child_items(self):
		for item in self.items:
			if frappe.db.exists("Product Bundle", item.item_code):
				frappe.throw(_("Row #{0}: Child Item should not be a Product Bundle. Please remove Item {1} and Save").format(item.idx, frappe.bold(item.item_code)))

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_new_item_code(doctype, txt, searchfield, start, page_len, filters):
	from erpnext.controllers.queries import get_match_cond

	return frappe.db.sql("""select name, item_name, description from tabItem
		where is_stock_item=0 and name not in (select name from `tabProduct Bundle`)
		and %s like %s %s limit %s, %s""" % (searchfield, "%s",
		get_match_cond(doctype),"%s", "%s"),
		("%%%s%%" % txt, start, page_len))


def update_bundle_price(doc, event):
    """
    doc: Product Bundle
    event: validate

    Calcular el precio del item padre segun los hijos.
    Buscar de cada item hijo las listas de precios y precio * cantidad
    Item1
        - Lista precio1
            item1_lista1 = precio * cantidad
        - Lista precio2
            item1_lista2 = precio * cantidad
    Item2
        - Lista precio1
            item2_lista1 = precio * cantidad
        - Lista precio2
            item2_lista2 = precio * cantidad

    Padre
        - Lista precio1
          precio = item1_lista1 + item2_lista1
         - Lista precio2
          precio = item1_lista2 + item2_lista2
    En el item padre crear los precios para cada lista
    """
    if not doc.create_price:
        return

    parent_item = frappe.get_doc('Item', doc.new_item_code)
    child_items = [frappe.get_doc('Item', item.item_code) for item in doc.items]

    qtys = {}

    price_lists_data = []

    for item in doc.items:
        qtys[item.item_code] = item.qty

    for child in child_items:
        price_lists = frappe.get_all('Item Price', filters={'item_code': child.item_code}, fields='DISTINCT(price_list) AS price_list')
        for price_list in price_lists:
            prices = get_item_price({"price_list": price_list['price_list'], 'uom': None, 'batch_no': None}, item_code=child.item_code, ignore_party=True)
            if prices:
                price_lists_data.append({
                    'item_code': child.item_code,
                    'price_list': price_list['price_list'],
                    'amount': prices[0][1] * qtys[child.item_code]
                })

    final_price_lists = {}

    for price in price_lists_data:
        if price['price_list'] in final_price_lists:
            final_price_lists[price['price_list']] += price['amount']
        else:
            final_price_lists[price['price_list']] = price['amount']

    for key, value in final_price_lists.items():
        item_price = frappe.get_all('Item Price', filters={'item_code': parent_item.item_code, 'price_list': key}, fields=['name'])
        if item_price:
            item_price = frappe.get_doc('Item Price', item_price[0]['name'])
            item_price.price_list_rate = value
            item_price.save()
            frappe.db.commit()
        else:
            item_price = frappe.get_doc({
                "doctype": "Item Price",
                "price_list": key,
                "item_code": parent_item.item_code,
                "price_list_rate": value
            })
            item_price.insert(ignore_permissions=True)


def update_item_bundle_price(doc, event):
    """
	doc: Item Price
    event: on_update
    """
    for bundle in frappe.get_all('Product Bundle Item', filters={'item_code': doc.item_code}, pluck='parent'):
        bundle = frappe.get_doc('Product Bundle', bundle)
        update_bundle_price(bundle, 'event')

 
