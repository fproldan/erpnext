// Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cierre de Caja', {
	onload: function(frm) {
		frm.set_query("user", function(doc) {
			return {
				filters: {"enabled": 1, "user_type": "System User"}
			};
		});

		frm.set_query("apertura_de_caja", function(doc) {
			return { filters: { 'status': 'Open', 'docstatus': 1 } };
		});

		if (frm.doc.docstatus === 0 && !frm.doc.amended_from) frm.set_value("period_end_date", frappe.datetime.now_datetime());

		set_html_data(frm);
	},

	refresh: function(frm) {
		if (frm.doc.docstatus == 1) {

			frm.add_custom_button('Mostrar Comprobantes', function () {
				
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
		frappe.call({
	        method: "erpnext.accounts.doctype.cierre_de_caja.cierre_de_caja.get_payment_reconciliation",
	        args: {apertura_de_caja: frm.doc.apertura_de_caja, period_start_date: frm.doc.period_start_date, period_end_date: frm.doc.period_end_date},
	        callback: (data) => {
	        	if (data.message) {
	        		var response = data.message;
	        		response.forEach(detail => {
						frm.add_child("payment_reconciliation", {
							mode_of_payment: detail.mode_of_payment,
							opening_amount: detail.opening_amount,
							expected_amount: detail.expected_amount
						});
					});
					frm.refresh_field("payment_reconciliation");
	        	}
	        }
	    });
	},

	before_save: function(frm) {
		frm.set_value("bill_total", 0);
		frm.set_value("total_cash_cheque", 0);

		frappe.call({
			method: "get_totals",
			doc: frm.doc,
			callback: (r) => {
				if (r.message) {
					frm.set_value("bill_total", r.message["bill_total"]);
					frm.set_value("total_cash_cheque", r.message["total_cash_cheque"]);
				}
			}
		});
	}

});

frappe.ui.form.on('Cierre de Caja Detail', {
	closing_amount: (frm, cdt, cdn) => {
		const row = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "difference", flt(row.expected_amount - row.closing_amount));
		frm.refresh_field("payment_reconciliation");
	}
})


function reset_values(frm) {
	frm.set_value("payment_reconciliation", []);
	frm.set_value("bill_total", 0);
	frm.set_value("total_cash_cheque", 0);
}

function refresh_fields(frm) {
	frm.refresh_field("payment_reconciliation");
	frm.refresh_field("bill_total");
	frm.refresh_field("total_cash_cheque");
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
