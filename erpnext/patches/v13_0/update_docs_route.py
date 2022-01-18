# Copyright (c) 2021, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe


def execute():
    doc_nav = frappe.get_doc("Navbar Item", frappe.get_all("Navbar Item", {"item_label": "Documentación"}, pluck="name")[0])
    doc_nav.route = "https://diamo.com.ar/doc"
    doc_nav.save()
    frappe.db.commit()
