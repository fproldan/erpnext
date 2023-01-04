from __future__ import unicode_literals

import frappe
from frappe import _
from erpnext.controllers.website_list_for_contact import get_customers_suppliers


def get_context(context):

	user = frappe.session.user

	contacts = frappe.db.sql("""
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

	if not contacts:
		frappe.throw(_("Not Permitted"), frappe.PermissionError)

	context.supplier = contacts[0]['link_name']
	context.usuario = contacts[0]['email_id']
	return context


