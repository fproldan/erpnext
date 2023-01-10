from __future__ import unicode_literals

import frappe
from frappe import _
from erpnext.controllers.website_list_for_contact import get_customers_suppliers


def get_context(context):

	contacts = get_contacts()

	if not contacts:
		frappe.throw(_("Not Permitted"), frappe.PermissionError)

	if not context.doc:
		context.supplier = contacts[0]['link_name']
		context.usuario = contacts[0]['email_id']

	if context.doc:
		context.status = context.doc.status
	else:
		context.status = 'Pendiente'
	return context


def get_contacts():
	user = frappe.session.user

	return frappe.db.sql("""
	select
		`tabContact`.email_id,
		`tabDynamic Link`.link_doctype,
		`tabDynamic Link`.link_name
	from
		`tabContact`, `tabDynamic Link`
	where
		`tabDynamic Link`.link_doctype="Supplier"
	and
		`tabContact`.name=`tabDynamic Link`.parent and `tabContact`.email_id =%s
	""", user, as_dict=1)



def get_list_context(context):
	context.get_list = get_solicitud_list #  query return the data to be render in lest 


def get_solicitud_list(doctype, txt, filters, limit_start, limit_page_length = 20, order_by='modified desc'):
	return frappe.get_all(doctype, filters={'usuario': frappe.session.user}, fields=['name', 'status', 'proveedor', 'usuario'])