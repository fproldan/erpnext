# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import unittest
from unittest.mock import MagicMock, patch

import frappe

from erpnext.stock.doctype.packed_item import packed_item


class PackingDocument:
	"""In-memory table operations; database lookups are mocked in these tests."""

	def __init__(self, **values):
		self.amended_from = None
		self.__dict__.update(values)

	def get(self, fieldname):
		return getattr(self, fieldname, None)

	def append(self, fieldname, values):
		row = frappe._dict(values)
		getattr(self, fieldname).append(row)
		return row

	def set(self, fieldname, value):
		setattr(self, fieldname, value)


class TestPackedItem(unittest.TestCase):
	def setUp(self):
		for name, value in (
			("get_product_bundle_items", [frappe._dict(item_code="Component", qty=4)]),
			("get_packing_item_details", frappe._dict(item_name="Component", stock_uom="Nos", is_stock_item=1)),
			("get_bin_qty", frappe._dict(actual_qty=100, projected_qty=100)),
		):
			mock = patch.object(packed_item, name, return_value=value)
			mock.start()
			self.addCleanup(mock.stop)

		db_patch = patch.object(packed_item.frappe, "db", MagicMock())
		db = db_patch.start()
		self.addCleanup(db_patch.stop)
		db.get_value.return_value = "Combo"
		db.get_single_value.return_value = 0

		self.doc = PackingDocument(company="Test Company", items=[], packed_items=[])
		for index, qty in enumerate((1, 2), 1):
			self.doc.append("items", {
				"name": "dn-item-{}".format(index),
				"item_code": "Combo",
				"stock_qty": qty,
				"conversion_factor": 1,
				"warehouse": "Stores",
				"against_sales_order": "SO-{}".format(index),
			})
			# Obtaining items from two OVs produces two unlinked packed rows.
			self.doc.append("packed_items", {
				"parent_item": "Combo", "item_code": "Component", "qty": qty * 4,
			})

	def test_same_bundle_from_two_sales_orders(self):
		packed_item.make_packing_list(self.doc)
		self.assertEqual(len(self.doc.packed_items), 2)
		self.assertEqual(
			{row.parent_detail_docname: row.qty for row in self.doc.packed_items},
			{"dn-item-1": 4, "dn-item-2": 8},
		)

		# Subsequent saves must retain the separate rows and their stock details.
		self.doc.packed_items[0].warehouse = "Other Stores"
		self.doc.packed_items[0].batch_no = "Batch A"
		self.doc.items[1].stock_qty = 3
		packed_item.make_packing_list(self.doc)
		self.assertEqual(len(self.doc.packed_items), 2)
		self.assertEqual([row.qty for row in self.doc.packed_items], [4, 12])
		self.assertEqual(self.doc.packed_items[0].warehouse, "Other Stores")
		self.assertEqual(self.doc.packed_items[0].batch_no, "Batch A")

	def test_removing_one_recurring_bundle(self):
		packed_item.make_packing_list(self.doc)
		self.doc.items.pop(0)
		packed_item.make_packing_list(self.doc)
		self.assertEqual(len(self.doc.packed_items), 1)
		self.assertEqual(self.doc.packed_items[0].parent_detail_docname, "dn-item-2")
		self.assertEqual(self.doc.packed_items[0].qty, 8)
