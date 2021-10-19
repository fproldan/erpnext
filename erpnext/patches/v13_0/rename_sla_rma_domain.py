# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe


def execute():
    if frappe.db.exists("Domain", "SLA y RMA"):
        if frappe.db.exists("Domain", "RMA"):
            frappe.db.delete("Domain", "SLA y RMA")
        else:
            frappe.db.set_value("Domain", "SLA y RMA", "domain", "RMA")
            frappe.db.set_value("Domain", "SLA y RMA", "name", "RMA")
