# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

def execute():
    subs = frappe.get_all('Subscription', {'naming_series': ''}, order_by='creation desc', pluck='name')
    if not subs:
        return

    for sub in subs:
        frappe.db.set_value('Subscription', sub, 'naming_series', 'ACC-SUB-.YYYY.-.#####')
    frappe.db.commit()