# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SolicitudCambiosProveedor(Document):
	pass


@frappe.whitelist()
def cambiar_estado(doctype, docname, estado):
	doc = frappe.get_doc(doctype, docname)
	frappe.db.set_value(doctype, docname, 'status', estado)
	return f'Estado de la solicitud {docname} modificada a: <b>{estado}</b>'