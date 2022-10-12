import frappe


@frappe.whitelist()
def get_stock(item_code, warehouse=None):
	from erpnext.stock.utils import get_latest_stock_qty

	if not frappe.db.exists('Item', item_code):
		return 'Producto inexistente'

	response = {
		'warehouses': [],
		'total': 0.0
	}
	total = 0.0
	qty_warehouse = 0.0

	if not warehouse:
		warehouses = frappe.db.get_all('Warehouse', filters={'is_group': 0}, fields=['name', 'company'])

	if warehouse:
		warehouses = frappe.db.get_all('Warehouse', filters=[['name', 'like', f'%{warehouse}%'], ['is_group', '=', 0]], fields=['name', 'company'])

	for warehouse in warehouses:
		qty_warehouse = get_latest_stock_qty(item_code, warehouse['name']) or 0.0
		warehouse.update({"qty": qty_warehouse})
		response['warehouses'].append(warehouse)
		total += qty_warehouse

	response['total'] = total
	return response


@frappe.whitelist()
def create_stock_entry(data):
	
	from_company = data.get("from_company")
	from_warehouse = data.get("from_warehouse")

	to_company = data.get("to_company")
	to_warehouse = data.get("to_warehouse")

	items = data.get("items")

	response = {}
	errors = []

	if not from_company:
		errors.append("Debe especificar la Compañía origen (from_company)")

	if not frappe.db.exists('Company', from_company):
		errors.append(f"Compañía origen {from_company} no existe (from_company)")

	if not from_warehouse:
		errors.append("Debe especificar el Almacén origen (from_warehouse)")

	if not frappe.db.exists('Warehouse', from_warehouse):
		errors.append("Almacén origen {from_warehouse} no existe (from_warehouse)")

	if to_company and not frappe.db.exists('Company', to_company):
		errors.append("Compañía destino {to_company} no existe (to_company)")

	if to_warehouse and not frappe.db.exists('Warehouse', to_warehouse):
		errors.append("Almacén destino {to_warehouse} no existe (to_warehouse)")

	if not items:
		errors.append("Debe especificar los productos (items)")

	for item in items:
		if not frappe.db.exists('Item', item['item_code']):
			errors.append(f"Producto {item['item_code']} no existe (items.item_code)")

	if errors:
		response['errors'] = errors
		return response

	receipt_stock_entry = None

	try:
		# Expedicion de Material
		issue_stock_entry = frappe.new_doc("Stock Entry")
		issue_stock_entry.purpose = "Material Issue"
		issue_stock_entry.company = from_company
		cost_center = frappe.get_value('Company', from_company, 'cost_center')
		expense_account = frappe.get_value('Company', from_company, 'stock_adjustment_account')

		for item_data in items:
			item = frappe.get_doc('Item', item_data['item_code'])
			issue_stock_entry.append("items", {
				"item_code": item.item_code,
				"s_warehouse": from_warehouse,
				"uom": item.stock_uom,
				"qty": item_data.get('qty') or 1,
				"conversion_factor": 1.0,  # TODO: conversion factor
				"transfer_qty": item_data.get('qty') * 1.0,  # TODO: conversion factor
				'cost_center': cost_center,
				'expense_account': expense_account,
			})

		issue_stock_entry.get_stock_and_rate()
		issue_stock_entry.set_stock_entry_type()
		issue_stock_entry.insert(ignore_permissions=True)
		issue_stock_entry.submit()

		if to_company and to_warehouse:
			# Recepcion de Material
			receipt_stock_entry = frappe.new_doc("Stock Entry")
			receipt_stock_entry.purpose = "Material Receipt"
			receipt_stock_entry.company = to_company
			cost_center = frappe.get_value('Company', to_company, 'cost_center')
			expense_account = frappe.get_value('Company', to_company, 'stock_adjustment_account')

			for item_data in items:
				item = frappe.get_doc('Item', item_data['item_code'])
				receipt_stock_entry.append("items", {
					"item_code": item.item_code,
					"t_warehouse": to_warehouse,
					"uom": item.stock_uom,
					"qty": item_data.get('qty') or 1,
					"conversion_factor": 1.0,  # TODO: conversion factor
					"transfer_qty": item_data.get('qty') * 1.0,  # TODO: conversion factor
					'cost_center': cost_center,
					'expense_account': expense_account,
				})

			receipt_stock_entry.get_stock_and_rate()
			receipt_stock_entry.set_stock_entry_type()
			receipt_stock_entry.insert(ignore_permissions=True)
			receipt_stock_entry.submit()

		frappe.db.commit()

		response = {
			'issue_stock_entry': issue_stock_entry.as_dict(),
			'receipt_stock_entry': receipt_stock_entry.as_dict() if receipt_stock_entry else {}
		}

		return response
	except Exception as e:
		response['errors'] = str(e)
		return response
	