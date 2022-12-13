// Copyright (c) 2022, Diamo and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lista de precios"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "price_list",
			"label": __("Lista de Precio"),
			"fieldtype": "Link",
			"options": "Price List",
		},
		{
			"fieldname": "item",
			"label": __("Producto"),
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname": "brand",
			"label": __("Marca"),
			"fieldtype": "Link",
			"options": "Brand",
		},
		{
			"fieldname": "purchase_user",
			"label": __("Usuario de compra predeterminado"),
			"fieldtype": "Link",
			"options": "User",
			"get_query": function() {
                return {
                    "doctype": "User",
                    "filters": {
                        "user_type": "System User",
                    }
                }
            }
		},
		{
			"fieldname": "historico",
			"label": __("Histórico"),
			"fieldtype": "Check",
		},
		{
			"fieldname": "al_dia",
			"label": __("Al día de hoy"),
			"fieldtype": "Check",
			"default": 1,
		},
	],
	"formatter": function(value, row, column, data, default_formatter) {
        if (column.fieldname=="price_list_rate") {
            value = "<b>"+default_formatter(value, row, column, data)+"</b>";
        	return value;
        } else {
        	return default_formatter(value, row, column, data);
        }
    },
};
