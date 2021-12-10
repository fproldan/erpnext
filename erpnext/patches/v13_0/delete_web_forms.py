# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe


def execute():
    for name in ["request-to-delete-data", "request-data", "student-applicant", "lab-test", "patient-registration", "prescription", "patient-appointments", "personal-details", "certification-application-usd", "certification-application", "grant-application"]:
        frappe.db.delete("Web Form", name)
    frappe.db.commit()
