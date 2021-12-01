# Copyright (c) 2021, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe


def execute():
    frappe.db.delete("Dashboard")
    frappe.db.delete("Number Card")
    frappe.db.delete("Dashboard Chart")
    frappe.db.delete("Dashboard Chart Link")
    frappe.db.commit()

    active_domains = [d.domain for d in frappe.get_doc('Domain Settings').active_domains]
    print(active_domains)
