# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe


def execute():
    if frappe.db.exists("Domain", "SLA y RMA"):
        frappe.db.delete("Domain", "SLA y RMA")
        frappe.db.commit()

    if not frappe.db.exists("Domain", "RMA"):
        d = frappe.new_doc('Domain')
        d.name = 'RMA'
        d.domain = 'RMA'
        d.save()
        frappe.db.commit()
