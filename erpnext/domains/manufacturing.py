from __future__ import unicode_literals

data = {
	'desktop_icons': [
		'Item',
		'BOM',
		'Customer',
		'Supplier',
		'Sales Order',
		'Purchase Order',
		'Work Order',
		'Task',
		'Accounts',
		'HR',
		'ToDo'
	],
	# 'restricted_roles': [
 #        'Manufacturing Manager',
 #        'Manufacturing User'
 #    ],
	'properties': [
		{'doctype': 'Item', 'fieldname': 'manufacturing', 'property': 'collapsible_depends_on', 'value': 'is_stock_item'},
	],
	'set_value': [
		['Stock Settings', None, 'show_barcode_field', 1]
	],
	'default_portal_role': 'Customer'
}
