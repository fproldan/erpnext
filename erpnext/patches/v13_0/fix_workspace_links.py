# Copyright (c) 2020, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

import frappe


def execute():
	frappe.db.sql("""
		DELETE FROM `tabWorkspace Shortcut`
		WHERE type = "Dashboard" AND link_to in ("Education", "Healthcare", "Human Resource", "Loan Dashboard", "Manufacturing", "Payroll");
	""")
	frappe.db.commit()