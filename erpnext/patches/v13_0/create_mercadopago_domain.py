from __future__ import unicode_literals

import frappe


def execute():
    d = frappe.new_doc('Domain')
    d.name = 'Mercadopago'
    d.domain = 'Mercadopago'
    d.save()
    frappe.db.commit()
