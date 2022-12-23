from __future__ import unicode_literals

import frappe
from frappe.model.utils.rename_field import rename_field


def execute():
	frappe.reload_doc("Accounts", "doctype", "Purchase Invoice")

	for pi in frappe.get_all('Purchase Invoice', filters={'condicion_de_iva_proveedor': ''}, fields='name,supplier'):
		supp = frappe.db.get_value('Supplier', pi['supplier'], ['tipo_de_documento_proveedor', 'condicion_de_iva_proveedor'], as_dict=True)
		frappe.db.set_value('Purchase Invoice', pi['name'], 'tipo_de_documento_proveedor', supp['tipo_de_documento_proveedor'])
		frappe.db.set_value('Purchase Invoice', pi['name'], 'condicion_de_iva_proveedor', supp['condicion_de_iva_proveedor'])
	frappe.db.commit()
