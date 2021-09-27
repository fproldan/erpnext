# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import get_link_to_form

from erpnext.controllers.status_updater import StatusUpdater


class AperturadeCaja(StatusUpdater):
    def validate(self):
        self.validate_payment_method_account()
        self.set_status()

    def validate_payment_method_account(self):
        invalid_modes = []
        for d in self.balance_details:
            if d.mode_of_payment:
                account = frappe.db.get_value("Mode of Payment Account", {"parent": d.mode_of_payment, "company": self.company}, "default_account")
                if not account:
                    invalid_modes.append(get_link_to_form("Mode of Payment", d.mode_of_payment))

        if invalid_modes:
            if invalid_modes == 1:
                msg = _("Please set default Cash or Bank account in Mode of Payment {}")
            else:
                msg = _("Please set default Cash or Bank account in Mode of Payments {}")
            frappe.throw(msg.format(", ".join(invalid_modes)), title=_("Missing Account"))

    def on_submit(self):
        self.set_status(update=True)
