// Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Apertura de Caja', {
	setup(frm) {
		if (frm.doc.docstatus == 0) {
			frm.trigger('set_posting_date_read_only');
			frm.set_value('period_start_date', frappe.datetime.now_datetime());
			frm.set_value('user', frappe.session.user);
			frm.refresh_field("user");
			show_hide_user(frm);
		}

		frm.set_query("user", function(doc) {
			return {
				filters: {
					"enabled": 1,
					"user_type": "System User"
				}
			};
		});
	},
	onload(frm) {
		if (frm.doc.docstatus == 0) {show_hide_user(frm);}
	},
	refresh(frm) {
		// set default posting date / time
		if(frm.doc.docstatus == 0) {
			if(!frm.doc.posting_date) {
				frm.set_value('posting_date', frappe.datetime.nowdate());
			}
			frm.trigger('set_posting_date_read_only');
			show_hide_user(frm);
		}
	},
	set_posting_date_read_only(frm) {
		if(frm.doc.docstatus == 0 && frm.doc.set_posting_date) {
			frm.set_df_property('posting_date', 'read_only', 0);
		} else {
			frm.set_df_property('posting_date', 'read_only', 1);
		}
	},
	set_posting_date(frm) {
		frm.trigger('set_posting_date_read_only');
	},
});


function has_admin_perms(frm) {
	return frappe.user.has_role('System Manager') || frappe.user.has_role('Accounts Manager') || frappe.user.has_role('Administrator');
}

function show_hide_user(frm) {
	if (!frm.doc.user) {
		frm.set_value('user', frappe.session.user);
		frm.refresh_field("user");
	}

	if (!has_admin_perms()) {
		frm.set_df_property('user', 'hidden', 1);
		frm.set_df_property('user', 'read_only', 1);
		frm.refresh_field("user");
	}
}