import frappe


@frappe.whitelist()
def get_stock(item_code, warehouse=None):
	from erpnext.stock.utils import get_latest_stock_qty

	if not frappe.db.exists('Item', item_code):
		return 'Producto inexistente'

	response = {}
	total = 0.0
	qty_warehouse = 0.0

	if not warehouse:
		warehouses = frappe.db.get_all('Warehouse', filters={'is_group': 0})

	if warehouse:
		if frappe.db.exists('Warehouse', warehouse):
			warehouses = [{'name': warehouse}]
		else:
			warehouses = frappe.db.get_all('Warehouse', filters=[['name', 'like', f'%{warehouse}%'], ['is_group', '=', 0]])

	for warehouse in warehouses:
		qty_warehouse = get_latest_stock_qty(item_code, warehouse['name']) or 0.0
		response[warehouse['name']] = qty_warehouse
		total += qty_warehouse

	response['total'] = total
	return response
