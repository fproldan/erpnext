// Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Process Sales Commission', {
	setup: function(frm) {
		frm.set_query("department", function() {
			if (!frm.doc.company) {
				frappe.throw(__("Please select company first"));
			}
			return {
				filters: {
					company: frm.doc.company
				}
			};
		});
		frm.set_query("commission_against", function() {
			return {
				filters: [
					['name', 'in', ["Canal de Venta"]]
				]
			};
		});
		frm.set_query("sales_persons", function() {
			return {
				filters: {"enabled": 1}
			};
		});
	},
	company: function(frm) {
		get_sales_persons(frm)
	},
	department: function(frm) {
		get_sales_persons(frm)
	},
	designation: function(frm) {
		get_sales_persons(frm)
	},
	branch: function(frm) {
		get_sales_persons(frm)
	}
});	


function get_sales_persons(frm) {
	frm.clear_table("sales_persons");
	return frappe.call({
		doc: frm.doc,
		method: 'get_sales_persons',
		callback: function () {
			frm.dirty();
			frm.refresh();
		},
	});
}