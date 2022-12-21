# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import _

from erpnext.e_commerce.doctype.e_commerce_settings.e_commerce_settings import show_attachments


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = frappe.get_doc(frappe.form_dict.doctype, frappe.form_dict.name)

	if show_attachments():
		context.attachments = get_attachments(frappe.form_dict.doctype, frappe.form_dict.name)

	context.parents = frappe.form_dict.parents
	context.title = frappe.form_dict.name

	default_print_format = frappe.db.get_value('Property Setter', dict(property='default_print_format', doc_type=frappe.form_dict.doctype), "value")
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"

	if not frappe.has_website_permission(context.doc):
		frappe.throw(_("Not Permitted"), frappe.PermissionError)

	# if frappe.form_dict.get('nuevo_pacto_entrega') and context.doc.doctype == 'Purchase Order':
	# 	context.doc.nuevo_pacto_entrega = frappe.form_dict.get('nuevo_pacto_entrega')
	# 	context.doc.save(ignore_permissions=True)
	# 	frappe.db.commit()


def get_attachments(dt, dn):
    return frappe.get_all("File", fields=["name", "file_name", "file_url", "is_private"], filters={"attached_to_name": dn, "attached_to_doctype": dt, "is_private":0})
