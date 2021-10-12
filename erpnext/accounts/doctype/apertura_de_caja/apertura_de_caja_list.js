// Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
frappe.listview_settings['Apertura de Caja'] = {
	get_indicator: function(doc) {
		var status_color = {
			"Draft": "red",
			"Open": "orange",
			"Closed": "green",
			"Cancelled": "red"
		};
		return [__(doc.status), status_color[doc.status], "status,=,"+doc.status];
	}
};
