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
    context.docname = context.doc.name
    if hasattr(context.doc, "set_indicator"):
        context.doc.set_indicator()

    if show_attachments() or context.doc.doctype in ['Purchase Order']:
        context.attachments = get_attachments(frappe.form_dict.doctype, frappe.form_dict.name)

    context.parents = frappe.form_dict.parents
    context.title = frappe.form_dict.name
    context.payment_ref = frappe.db.get_value("Payment Request", {"reference_name": frappe.form_dict.name}, "name")

    context.enabled_checkout = frappe.get_doc("E Commerce Settings").enable_checkout

    default_print_format = frappe.db.get_value('Property Setter', dict(property='default_print_format', doc_type=frappe.form_dict.doctype), "value")
    if default_print_format:
        context.print_format = default_print_format
    else:
        context.print_format = "Standard"

    if not frappe.has_website_permission(context.doc):
        frappe.throw(_("Not Permitted"), frappe.PermissionError)

    # check for the loyalty program of the customer
    if context.doc.get('customer'):
        customer_loyalty_program = frappe.db.get_value("Customer", context.doc.customer, "loyalty_program")
        if customer_loyalty_program:
            from erpnext.accounts.doctype.loyalty_program.loyalty_program import get_loyalty_program_details_with_points
            loyalty_program_details = get_loyalty_program_details_with_points(context.doc.customer, customer_loyalty_program)
            context.available_loyalty_points = int(loyalty_program_details.get("loyalty_points"))

    if context.doc.doctype == 'Purchase Order':
        if frappe.form_dict.get('nuevo_pacto_entrega'):
            context.doc.nuevo_pacto_entrega = frappe.form_dict.get('nuevo_pacto_entrega')
            context.doc.save(ignore_permissions=True)
            frappe.db.commit()

        if frappe.form_dict.get('aprobar_rechazar_por_proveedor'):
            if frappe.form_dict.get('aprobar_rechazar_por_proveedor') == 'aprobar':
                context.doc.aprobado_por_proveedor = 1
                context.doc.save(ignore_permissions=True)
                frappe.db.commit()
                context.doc.set_status(update=True)
                frappe.db.commit()

            if frappe.form_dict.get('aprobar_rechazar_por_proveedor') == 'rechazar':
                context.doc.flags.ignore_permissions = True
                context.doc.cancel()
                frappe.db.set_value(context.doc.doctype, context.doc.name, 'motivo_de_rechazo', 'Cancelado por Proveedor')
                frappe.db.commit()

def get_attachments(dt, dn):
    return frappe.get_all("File", fields=["name", "file_name", "file_url", "is_private"], filters={"attached_to_name": dn, "attached_to_doctype": dt, "is_private": 0})


@frappe.whitelist(allow_guest=True)
def attach_file_to_po(files, docname):
    import json
    from frappe.utils.file_manager import save_file
    
    if files:
        fd_json = json.loads(files)
        fd_list = list(fd_json["files_data"])
        for fd in fd_list:
            save_file(fd["filename"], fd["dataurl"], "Purchase Order", docname, decode=True, is_private=0)
            frappe.db.commit()


