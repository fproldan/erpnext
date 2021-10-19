// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
frappe.query_reports["Detalle de Cierre de Caja"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Datetime",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"mode_of_payment",
			"label": __("Mode of Payment"),
			"fieldtype": "MultiSelectList",
			"options": "Mode of Payment",
			"reqd": 1,
			get_data: function(txt) {
				return frappe.db.get_link_options('Mode of Payment', txt, {
					company: frappe.query_report.get_filter_value("company")
				});
			}
		},
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == 'payments') {
			console.log(data)
			if (data !== undefined && data[column.fieldname] !== null && data['signo'] < 0) {
				return "<span style='color:red'>" + value + "</span>";
			}
		}

		return value;
	}
};
