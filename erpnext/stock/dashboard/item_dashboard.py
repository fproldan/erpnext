from __future__ import unicode_literals

import frappe
from frappe.model.db_query import DatabaseQuery
from frappe.utils import cint, flt


@frappe.whitelist()
def get_data(item_code=None, warehouse=None, item_group=None, purchase_user=None,
	start=0, sort_by='actual_qty', sort_order='desc'):
	'''Return data to render the item dashboard'''
	filters = []
	if item_code:
		filters.append(['item_code', '=', item_code])
	if warehouse:
		filters.append(['warehouse', '=', warehouse])
	if item_group:
		lft, rgt = frappe.db.get_value("Item Group", item_group, ["lft", "rgt"])
		items = frappe.db.sql_list("""
			select i.name from `tabItem` i
			where exists(select name from `tabItem Group`
				where name=i.item_group and lft >=%s and rgt<=%s)
		""", (lft, rgt))
		filters.append(['item_code', 'in', items])

	try:
		# check if user has any restrictions based on user permissions on warehouse
		if DatabaseQuery('Warehouse', user=frappe.session.user).build_match_conditions():
			filters.append(['warehouse', 'in', [w.name for w in frappe.get_list('Warehouse')]])
	except frappe.PermissionError:
		# user does not have access on warehouse
		return []

	items = frappe.db.get_all('Bin', fields=['item_code', 'warehouse', 'projected_qty', 'reserved_qty', 'reserved_qty_for_production', 'reserved_qty_for_sub_contract', 'actual_qty', 'valuation_rate'],
		or_filters={
			'projected_qty': ['!=', 0],
			'reserved_qty': ['!=', 0],
			'reserved_qty_for_production': ['!=', 0],
			'reserved_qty_for_sub_contract': ['!=', 0],
			'actual_qty': ['!=', 0],
		},
		filters=filters,
		order_by=sort_by + ' ' + sort_order,
		limit_start=start,
		limit_page_length='21')

	precision = cint(frappe.db.get_single_value("System Settings", "float_precision"))

	for item in items:
		company = frappe.get_cached_value("Warehouse", item.warehouse, 'company')
		item_purchase_user = frappe.db.get_value("Item Default", {"parent": item.item_code, "company": company}, 'purchase_user')
		item_group = frappe.get_cached_value("Item", item.item_code, 'item_group')
		item_group_purchase_user = frappe.db.get_value("Item Default", {"parent": item_group, "company": company}, 'purchase_user')
		item_purchase_user = item_purchase_user or item_group_purchase_user
		item.update({
			'purchase_user': item_purchase_user,
			'item_name': frappe.get_cached_value("Item", item.item_code, 'item_name'),
			'disable_quick_entry': frappe.get_cached_value("Item", item.item_code, 'has_batch_no') or frappe.get_cached_value("Item", item.item_code, 'has_serial_no'),
			'projected_qty': flt(item.projected_qty, precision),
			'reserved_qty': flt(item.reserved_qty, precision),
			'reserved_qty_for_production': flt(item.reserved_qty_for_production, precision),
			'reserved_qty_for_sub_contract': flt(item.reserved_qty_for_sub_contract, precision),
			'actual_qty': flt(item.actual_qty, precision),
		})

	if purchase_user:
		return [item for item in items if item['purchase_user'] == purchase_user]
	return items
