# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.utils import cint, quoted
from frappe.website.render import resolve_path
from frappe.model.document import get_controller, Document
from frappe import _
from frappe.modules.utils import get_module_app
from frappe.utils import flt, has_common
from frappe.utils.user import is_website_user
from erpnext.controllers.website_list_for_contact import *


def get_context(context, **dict_params):
    """Returns context for a list standard list page.
    Will also update `get_list_context` from the doctype module file"""
    frappe.local.form_dict.update(dict_params)
    frappe.local.form_dict.doctype = 'Purchase Invoice'
    doctype = frappe.local.form_dict.doctype
    context.companies = frappe.get_all('Company', filters={'exclude_in_portal': 0}, fields='name')
    context.title = 'Facturas de compra'
    context.parents = [{"route":"me", "title":_("My Account")}]
    context.show_sidebar = True
    context.show_search = True
    context.no_cache = 1
    context.meta = frappe.get_meta(doctype)
    context.update(get_list_context(context, doctype) or {})
    context.doctype = doctype
    context.company = frappe.local.form_dict.company
    context.txt = frappe.local.form_dict.txt
    context.bill_no = frappe.local.form_dict.bill_no
    context.posting_date = frappe.local.form_dict.posting_date
    context.bill_date = frappe.local.form_dict.bill_date
    context.status = frappe.local.form_dict.status
    frappe.local.form_dict.fields = ['name', 'docstatus', 'posting_date', 'bill_date']
    context.update(get(**frappe.local.form_dict))
    context.template = 'templates/pages/purchase_invoices.html'
    context.list_template = 'templates/pages/purchase_invoices_list.html'
    

@frappe.whitelist(allow_guest=True)
def get(doctype, company=None, txt=None, bill_no=None, posting_date=None, status=None, bill_date=None, limit_start=0, limit=20, pathname=None, **kwargs):
    """Returns processed HTML page for a standard listing."""
    limit_start = cint(limit_start)

    raw_result = get_list_data(doctype, company, txt, bill_no, posting_date, status, bill_date, limit_start, limit=limit + 1, **kwargs)
    show_more = len(raw_result) > limit
    if show_more:
        raw_result = raw_result[:-1]

    meta = frappe.get_meta(doctype)
    list_context = frappe.flags.list_context

    if not raw_result: return {"result": []}

    result = []
    row_template = 'templates/pages/purchase_invoices_row.html'
    list_view_fields = [df for df in meta.fields if df.fieldname in ['title', 'status', 'posting_date']]

    for doc in raw_result:
        doc.doctype = doctype
        new_context = frappe._dict(doc=doc, meta=meta, list_view_fields=list_view_fields)

        if not list_context.get_list and not isinstance(new_context.doc, Document):
            new_context.doc = frappe.get_doc(doc.doctype, doc.name)
            new_context.update(new_context.doc.as_dict())

        if not frappe.flags.in_test:
            pathname = pathname or frappe.local.request.path
            new_context["pathname"] = pathname.strip("/ ")
        new_context.update(list_context)
        set_route(new_context)
        rendered_row = frappe.render_template(row_template, new_context, is_path=True)
        result.append(rendered_row)

    from frappe.utils.response import json_handler
    return {
        "raw_result": json.dumps(raw_result, default=json_handler),
        "result": result,
        "show_more": show_more,
        "next_start": limit_start + limit,
    }

@frappe.whitelist(allow_guest=True)
def get_list_data(doctype, company=None, txt=None, bill_no=None, posting_date=None, status=None, bill_date=None, limit_start=0, fields=None, cmd=None, limit=20, web_form_name=None, **kwargs):
    """Returns processed HTML page for a standard listing."""
    limit_start = cint(limit_start)

    if not txt and frappe.form_dict.search:
        txt = frappe.form_dict.search
        del frappe.form_dict['search']

    controller = get_controller(doctype)
    meta = frappe.get_meta(doctype)

    filters = prepare_filters(doctype, controller, kwargs)
    list_context = get_list_context(frappe._dict(), doctype, web_form_name)
    list_context.title_field = getattr(controller, 'website', {}).get('page_title_field', meta.title_field or 'name')

    if list_context.filters:
        filters.update(list_context.filters)

    kwargs = dict(
        doctype=doctype, company=company, txt=txt, bill_no=bill_no, posting_date=posting_date, status=status, bill_date=bill_date, filters=filters,
        limit_start=limit_start, limit_page_length=limit,
        order_by=list_context.order_by or 'modified desc'
    )

    # allow guest if flag is set
    if not list_context.get_list and (list_context.allow_guest or meta.allow_guest_to_view):
        kwargs['ignore_permissions'] = True

    raw_result = get_transaction_list(**kwargs)

    # list context to be used if called as rendered list
    frappe.flags.list_context = list_context

    return raw_result

def set_route(context):
    '''Set link for the list item'''
    if context.web_form_name:
        context.route = "{0}?name={1}".format(context.pathname, quoted(context.doc.name))
    elif context.doc and getattr(context.doc, 'route', None):
        context.route = context.doc.route
    else:
        context.route = "{0}/{1}".format(context.pathname or quoted(context.doc.doctype),
            quoted(context.doc.name))

def prepare_filters(doctype, controller, kwargs):
    for key in kwargs.keys():
        try:
            kwargs[key] = json.loads(kwargs[key])
        except ValueError:
            pass
    filters = frappe._dict(kwargs)
    meta = frappe.get_meta(doctype)

    if hasattr(controller, 'website') and controller.website.get('condition_field'):
        filters[controller.website['condition_field']] = 1

    if filters.pathname:
        # resolve additional filters from path
        resolve_path(filters.pathname)
        for key, val in frappe.local.form_dict.items():
            if key not in filters and key != 'flags':
                filters[key] = val

    # filter the filters to include valid fields only
    for fieldname, val in list(filters.items()):
        if not meta.has_field(fieldname):
            del filters[fieldname]

    return filters

def get_list_context(context, doctype, web_form_name=None):
    from frappe.modules import load_doctype_module

    list_context = context or frappe._dict()
    meta = frappe.get_meta(doctype)

    def update_context_from_module(module, list_context):
        # call the user defined method `get_list_context`
        # from the python module
        if hasattr(module, "get_list_context"):
            out = frappe._dict(module.get_list_context(list_context) or {})
            if out:
                list_context = out
        return list_context

    # get context from the doctype module
    if not meta.custom:
        # custom doctypes don't have modules
        module = load_doctype_module(doctype)
        list_context = update_context_from_module(module, list_context)

    # get context for custom webform
    if meta.custom and web_form_name:
        webform_list_contexts = frappe.get_hooks('webform_list_context')
        if webform_list_contexts:
            out = frappe._dict(frappe.get_attr(webform_list_contexts[0])(meta.module) or {})
            if out:
                list_context = out

    # get context from web form module
    if web_form_name:
        web_form = frappe.get_doc('Web Form', web_form_name)
        list_context = update_context_from_module(web_form.get_web_form_module(), list_context)

    # get path from '/templates/' folder of the doctype
    if not meta.custom and not list_context.row_template:
        list_context.row_template = meta.get_row_template()

    if not meta.custom and not list_context.list_template:
        list_context.template = meta.get_list_template() or "www/list.html"

    return list_context


def get_transaction_list(doctype, company=None, txt=None, bill_no=None, posting_date=None, status=None, bill_date=None, filters=None, limit_start=0, limit_page_length=20, order_by="modified", custom=False):
    user = frappe.session.user
    ignore_permissions = False

    if not filters: filters = []

    filters.append((doctype, 'docstatus', '=', 1))

    if (user != 'Guest' and is_website_user()):
        parties_doctype = doctype
        # find party for this contact
        customers, suppliers = get_customers_suppliers(parties_doctype, user)

        if customers:
            if doctype == 'Quotation':
                filters.append(('quotation_to', '=', 'Customer'))
                filters.append(('party_name', 'in', customers))
            else:
                filters.append(('customer', 'in', customers))
        elif suppliers:
            if doctype == 'Payment Entry':
                filters.append(('party', 'in', suppliers))
            elif doctype == 'Purchase Invoice':
                filters.append(('supplier', 'in', suppliers))
        elif not custom:
            return []

        # Since customers and supplier do not have direct access to internal doctypes
        ignore_permissions = True

        if not customers and not suppliers and custom:
            ignore_permissions = False
            filters = []

    transactions = get_list_for_transactions(doctype, txt, filters, limit_start, limit_page_length,
        fields='name', ignore_permissions=ignore_permissions, order_by='modified desc', bill_no=bill_no, posting_date=posting_date, company=company, status=status, bill_date=bill_date)

    if custom:
        return transactions

    return post_process(doctype, transactions)