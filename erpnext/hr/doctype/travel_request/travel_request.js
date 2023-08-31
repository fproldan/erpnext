// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Travel Request', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Employee Advance"), function() {
     			frappe.call({
					method: "erpnext.hr.doctype.travel_request.travel_request.make_employee_advance",
					args: {
						"dt": frm.doc.doctype,
						"dn": frm.doc.name
					},
					callback: function(r) {
						var doclist = frappe.model.sync(r.message);
						frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
					}
				});
     		}, __('Create'));

			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
	},
});
