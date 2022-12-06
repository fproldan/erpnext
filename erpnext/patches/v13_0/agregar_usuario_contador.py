# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from six import iteritems

from erpnext.setup.install import create_usuario_contador


def execute():
	create_usuario_contador()
	frappe.db.commit()
