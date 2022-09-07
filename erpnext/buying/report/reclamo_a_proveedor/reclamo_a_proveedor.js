// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Reclamo a Proveedor"] = {
	"filters": [
		{
		   "fieldname": "supplier",
		   "fieldtype": "Link",
		   "options": "Supplier",
		   "label": "Proveedor",
		},
		{
		   "fieldname": "schedule_date",
            "label": "Fecha de Entrega",
            "fieldtype": "Date"
       	},
		{
            "fieldname": "reclamado",
            "label": "Fecha de Reclamo",
            "fieldtype": "Date"
        },
	]
};
