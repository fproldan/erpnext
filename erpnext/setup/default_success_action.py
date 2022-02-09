from __future__ import unicode_literals

from frappe import _

doctype_list = [
	'Purchase Receipt',
	'Purchase Invoice',
	'Quotation',
	'Sales Order',
	'Delivery Note',
	'Sales Invoice'
]

def get_message(doctype):
	doc_map = {
		'Purchase Receipt': 'Recibo de compra',
		'Purchase Invoice': 'Factura de compra',
		'Quotation': 'Cotización',
		'Sales Order': 'Órden de venta',
		'Delivery Note': 'Nota de entrega',
		'Sales Invoice': 'Factura de venta',
	}
	return f"{doc_map[doctype]} validada con éxito"

def get_first_success_message(doctype):
	return get_message(doctype)

def get_default_success_action():
	return [{
		'doctype': 'Success Action',
		'ref_doctype': doctype,
		'message': get_message(doctype),
		'first_success_message': get_first_success_message(doctype),
		'next_actions': 'new\nprint\nemail'
	} for doctype in doctype_list]
