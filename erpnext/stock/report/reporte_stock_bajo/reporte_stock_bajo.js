// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Reporte Stock Bajo"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_default("company")
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "MultiSelectList",
			"width": "100",
			get_data: function(txt) {
				return frappe.db.get_link_options('Warehouse', txt);
			}
		},
		{
			"fieldname": "item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"width": "100",
		},
		{
			"fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
			"width": "100",
		},
		{
			"fieldname": "only_shortage",
			"label": __("Solo Bajos de Stock"),
			"fieldtype": "Check",
		},
		{
			"fieldname": "group_by_item",
			"label": __("Sumarizado por producto"),
			"fieldtype": "Check",
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
   	
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "low_stock" && data.low_stock < 1) {
			value = `<div style="color:red">${value}</div>`;
		}

		return value;
	},
};
