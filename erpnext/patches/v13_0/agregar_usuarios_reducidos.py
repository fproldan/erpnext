# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from six import iteritems

from erpnext.setup.install import add_usuarios_reducidos_user_types


def execute():
	frappe.flags.ignore_select_perm = True
	frappe.flags.update_select_perm_after_migrate = True
	add_usuarios_reducidos_user_types()
