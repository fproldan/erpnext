# Copyright (c) 2021, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe


def execute():
    frappe.db.delete("Dashboard")
    frappe.db.delete("Number Card")
    frappe.db.delete("Dashboard Chart")
    frappe.db.delete("Dashboard Chart Link")
    frappe.db.delete("Number Card Link")
    frappe.db.commit()

    active_domains = [d.domain for d in frappe.get_doc('Domain Settings').active_domains]
    if "Projects" in active_domains:
        from erpnext.projects.setup import add_dashboard
        add_dashboard()

    if "CRM" in active_domains:
        from erpnext.crm.setup import add_dashboard
        add_dashboard()

    if "Assets" in active_domains:
        from erpnext.assets.setup import add_dashboard
        add_dashboard()

    frappe.db.commit()
