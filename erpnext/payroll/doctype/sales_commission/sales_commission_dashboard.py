from __future__ import unicode_literals


def get_data():
	return {
		'fieldname': 'name',
		'non_standard_fieldnames': {
			'Payment Entry': 'reference_name',
		},
		'transactions': [
			{
				'items': ['Process Sales Commission', 'Payment Entry']
			},
		],
		'internal_links': {
			'Process Sales Commission': ['contributions', 'process_sales_commission'],
		},
		
	}