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


@frappe.whitelist()
def create_stock_entry(data):
	print(data)

	if False:
		# Expedicion de Material
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = "Material Issue"
		stock_entry.company = self.company

		for item in self.items:
			stock_entry.append("items", {
				"item_code": item.item_code,
				"s_warehouse": item.warehouse or self.set_warehouse,
				"qty": item.received_qty,
				"basic_rate": item.base_rate,
				"conversion_factor": item.conversion_factor or 1.0,
				"transfer_qty": flt(item.received_qty) * (flt(item.conversion_factor) or 1.0),
				"serial_no": item.serial_no,
				'batch_no': item.batch_no,
				'cost_center': item.cost_center,
				'expense_account': item.expense_account,
				'reference_purchase_receipt': self.name
			})

		stock_entry.set_stock_entry_type()
		stock_entry.insert(ignore_permissions=True)
		stock_entry.submit()

		# Recepcion de Material
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = "Material Receipt"
		stock_entry.company = self.to_company
		cost_center = frappe.get_value('Company', self.to_company, 'cost_center')
		expense_account = frappe.get_value('Company', self.to_company, 'stock_adjustment_account')

		for item in self.items:
			stock_entry.append("items", {
				"item_code": item.item_code,
				"t_warehouse": self.to_company_warehouse,
				"qty": item.received_qty,
				"basic_rate": item.base_rate,
				"conversion_factor": item.conversion_factor or 1.0,
				"transfer_qty": flt(item.received_qty) * (flt(item.conversion_factor) or 1.0),
				"serial_no": item.serial_no,
				'batch_no': item.batch_no,
				'cost_center': cost_center,
				'expense_account': expense_account,
				'reference_purchase_receipt': self.name
			})

		stock_entry.set_stock_entry_type()
		stock_entry.insert(ignore_permissions=True)
		stock_entry.submit()
	return 'SE'