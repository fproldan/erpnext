// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tablero de solicitudes"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
		},
		{
			"fieldname": "name",
			"label": __("Identificador"),
			"fieldtype": "Data",
		},
		{
			"fieldname": "title",
			"label": __("Nombre"),
			"fieldtype": "Data",
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": [null, __("Draft"), __("Submitted"), __("Stopped"), __("Cancelled"), __("Pending"), __("Partially Ordered"), __("Partially Received"), __("Ordered"), __("Issued"), __("Transferred"), __("Received")],
			"width": "80",
		},
		{
			"fieldname": "material_request_type",
			"label": __("Propósito"),
			"fieldtype": "Select",
			"options": [null, __("Purchase"), __("Material Transfer"), __("Material Issue")],
			"width": "80",
		}
	]
};
