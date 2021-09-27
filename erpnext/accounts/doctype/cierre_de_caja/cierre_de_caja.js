// Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cierre de Caja', {
	onload: function(frm) {
		frm.ignore_doctypes_on_cancel_all = ['POS Invoice Merge Log'];
	
		frm.set_query("user", function(doc) {
			return {
				filters: {
					"enabled": 1,
					"user_type": "System User"
				}
			};
		});

		frm.set_query("apertura_de_caja", function(doc) {
			return { filters: { 'status': 'Open', 'docstatus': 1 } };
		});

		if (frm.doc.docstatus === 0 && !frm.doc.amended_from) frm.set_value("period_end_date", frappe.datetime.now_datetime());

		frappe.realtime.on('closing_process_complete', async function(data) {
			await frm.reload_doc();
			if (frm.doc.status == 'Failed' && frm.doc.error_message && data.user == frappe.session.user) {
				frappe.msgprint({
					title: __('Falló el Cierre de Caja'),
					message: frm.doc.error_message,
					indicator: 'orange',
					clear: true
				});
			}
		});

		set_html_data(frm);
	},

	refresh: function(frm) {
		if (frm.doc.docstatus == 1 && frm.doc.status == 'Failed') {
			const issue = '<a id="jump_to_error" style="text-decoration: underline;">issue</a>';
			frm.dashboard.set_headline('El Cierre de Caja falló mientras se ejecutaba en segundo plano. Puede reolver el error {0} y reintentar el proceso.', [issue]);

			$('#jump_to_error').on('click', (e) => {
				e.preventDefault();
				frappe.utils.scroll_to(
					cur_frm.get_field("error_message").$wrapper,
					true,
					30
				);
			});

			frm.add_custom_button(__('Retry'), function () {
				frm.call('retry', {}, () => {
					frm.reload_doc();
				});
			});
		}
	},

	apertura_de_caja(frm) {
		if (frm.doc.apertura_de_caja && frm.doc.period_start_date && frm.doc.period_end_date && frm.doc.user) {
			reset_values(frm);
			frm.trigger("set_opening_amounts");
		}
	},

	set_opening_amounts(frm) {
		frappe.db.get_doc("Apertura de Caja", frm.doc.apertura_de_caja)
			.then(({ balance_details }) => {
				balance_details.forEach(detail => {
					frm.add_child("payment_reconciliation", {
						mode_of_payment: detail.mode_of_payment,
						opening_amount: detail.opening_amount,
						expected_amount: detail.opening_amount
					});
				})
				frm.refresh_field("payment_reconciliation");
			});
	},


	before_save: function(frm) {
		frm.set_value("grand_total", 0);
		frm.set_value("net_total", 0);
		frm.set_value("total_quantity", 0);
		frm.set_value("taxes", []);

		for (let row of frm.doc.payment_reconciliation) {
			row.expected_amount = row.opening_amount;
		}
	}
});

frappe.ui.form.on('Cierre de Caja Detail', {
	closing_amount: (frm, cdt, cdn) => {
		const row = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "difference", flt(row.expected_amount - row.closing_amount));
	}
})


function reset_values(frm) {
	frm.set_value("payment_reconciliation", []);
	frm.set_value("taxes", []);
	frm.set_value("grand_total", 0);
	frm.set_value("net_total", 0);
	frm.set_value("total_quantity", 0);
}

function refresh_fields(frm) {
	frm.refresh_field("payment_reconciliation");
	frm.refresh_field("taxes");
	frm.refresh_field("grand_total");
	frm.refresh_field("net_total");
	frm.refresh_field("total_quantity");
}

function set_html_data(frm) {
	if (frm.doc.docstatus === 1 && frm.doc.status == 'Submitted') {
		frappe.call({
			method: "get_payment_reconciliation_details",
			doc: frm.doc,
			callback: (r) => {
				frm.get_field("payment_reconciliation_details").$wrapper.html(r.message);
			}
		});
	}
}
