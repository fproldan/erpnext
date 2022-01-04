# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe


def execute():
    titles = [
        {'title': 'Prescription'},
        {'title': 'Personal Details'},
        {'title': 'Fees'},
        {'title': 'Admission'},
        {'title': 'Patient Appointment'},
        {'title': 'Certification'},
        {'title': 'Lab Test'},
    ]

    for title in titles:
        frappe.db.delete("Portal Menu Item", {'title': title['title']})
    frappe.db.commit()
