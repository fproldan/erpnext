# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

def execute():
    subs = frappe.get_all('Subscription', order_by='creation desc', pluck='name')
    if not subs:
        return

    sub = subs[0].split('-')
    prefix = f'ACC-SUB-{sub[2]}-'
    number = int(sub[3])

    frappe.db.sql("update `tabSeries` set current = %s where name = %s", (number, prefix))
    frappe.db.commit()