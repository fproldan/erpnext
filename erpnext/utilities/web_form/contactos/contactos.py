from __future__ import unicode_literals

import frappe
from frappe import _


def get_context(context):
	# do your magic here
	from erpnext.controllers.website_list_for_contact import get_customers_suppliers

	context.show_sidebar = True

	if frappe.session.user == 'Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

	# context.supplier = None
	# customers, suppliers = get_customers_suppliers('Supplier', frappe.session.user)

	# if suppliers:
	# 	if frappe.form_dict.name not in suppliers:
	# 		frappe.throw(_("Not Permitted"), frappe.PermissionError)
	# else:
	# 	frappe.throw(_("Not Permitted"), frappe.PermissionError)
