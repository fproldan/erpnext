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

	frappe.db.set_value('User Type', 'Usuario de Ventas Reducido', 'role', 'Usuario Reducido Ventas')
	frappe.db.set_value('User Type', 'Usuario de Proyecto Reducido', 'role', 'Usuario Reducido Proyecto')
	frappe.db.set_value('User Type', 'Usuario de Soporte Reducido', 'role', 'Usuario Reducido Soporte')


	uv = frappe.get_all('User', {'user_type': 'Usuario de Ventas Reducido'})
	up = frappe.get_all('User', {'user_type': 'Usuario de Proyecto Reducido'})
	us = frappe.get_all('User', {'user_type': 'Usuario de Soporte Reducido'})


	for u in uv:
		user = frappe.get_doc('User', u['name'])
		for role in user.roles:
			if role.role == 'Sales User':
				role.role = 'Usuario Reducido Ventas'
				role.save()

	for u in up:
		user = frappe.get_doc('User', u['name'])
		for role in user.roles:
			if role.role == 'Projects User':
				role.role = 'Usuario Reducido Proyecto'
				role.save()

	for u in us:
		user = frappe.get_doc('User', u['name'])
		for role in user.roles:
			if role.role == 'Support Team':
				role.role = 'Usuario Reducido Soporte'
				role.save()