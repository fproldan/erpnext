from __future__ import unicode_literals

import frappe


def execute():
    frappe.get_doc(
        {
            "name": "¡Nueva actualización 1.4!",
            "title": "¡Nueva actualización 1.4 🚀 !",
            "public": 1,
            "notify_on_login": 1,
            "notify_on_every_login": 0,
            "expire_notification_on": "2022-05-15",
            "content": "",
            "doctype": "Note",
        }
    ).insert(ignore_mandatory=True)
    frappe.db.commit()
