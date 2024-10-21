// Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Commission', {
	onload: function(frm) {
		frm.ignore_doctypes_on_cancel_all = ['Payment Entry'];
	},
	setup: function(frm) {
		frm.set_query("commission_based_on", function() {
			return {
				filters: [
					['name', 'in', ["Sales Order", "Sales Invoice"]]
				]
			};
		});
		frm.set_query("commission_against", function() {
			return {
				filters: [
					['name', 'in', ["Canal de Venta"]]
				]
			};
		});
	},
	refresh: function(frm) {
		if (frm.doc.docstatus == 1) {
			if (frm.custom_buttons) frm.clear_custom_buttons();
			frm.events.add_context_buttons(frm);
		}
		if(frm.doc.docstatus > 0) {
			frm.add_custom_button(__('Ledger'), function() {
				frappe.route_options = {
					"voucher_no": frm.doc.name,
					"from_date": moment(frm.doc.creation).format('YYYY-MM-DD'),
					"to_date": moment(frm.doc.modified).format('YYYY-MM-DD'),
					"company": frm.doc.company,
					"group_by": "",
					"show_cancelled_entries": frm.doc.docstatus === 2
				};
				frappe.set_route("query-report", "General Ledger");
			}, "fa fa-table");
		}
		setTimeout(function() {
            toggleColumns(frm, ['commission_filter'], 'contributions', !frm.doc.omit_sales_person_transactions);
			toggleColumns(frm, ['order_or_invoice', 'posting_date'], 'contributions', frm.doc.omit_sales_person_transactions);
        }, 500);
	},
	omit_sales_person_transactions: function(frm) {
		toggleColumns(frm, ['commission_filter'], 'contributions', !frm.doc.omit_sales_person_transactions);
		toggleColumns(frm, ['order_or_invoice', 'posting_date'], 'contributions', frm.doc.omit_sales_person_transactions);
	},
	sales_person: function (frm) {
		frm.clear_table('contributions');
		frm.refresh();
	},
	get_contributions: function (frm) {
		frm.clear_table("contributions");
		return frappe.call({
			doc: frm.doc,
			method: 'add_contributions',
			callback: function () {
				frm.dirty();
				frm.save();
				frm.refresh();
			},
		});
	},

	add_context_buttons: function (frm) {
		if (!frm.doc.reference_name) {
			if (frm.doc.pay_via_salary) {
				frm.add_custom_button(__("Create Additional Salary"), function () {
					create_additional_salary(frm);
				}).addClass("btn-primary");
			} else {
				frm.add_custom_button(__("Create Payment Entry"), function () {
					create_payment_entry(frm);
				}).addClass("btn-primary");
			}
		}
	},
});


function toggleColumns(frm, fields, table, hidden) {
	let grid = frm.get_field(table).grid

	for (let field of fields) {
		grid.fields_map[field].hidden = hidden
	}

	grid.visible_columns = undefined
	grid.setup_visible_columns()
	grid.header_row.wrapper.remove()
	delete grid.header_row
	grid.make_head()

	for (let row of grid.grid_rows) {
		if (row.open_form_button) {
			row.open_form_button.parent().remove()
			delete row.open_form_button
		}

		for (let field in row.columns) {
			if (row.columns[field] !== undefined) {
				row.columns[field].remove()
			}
		}
		delete row.columns
		row.columns = []
		row.render_row()
	}
	frm.get_field(table).refresh()
}

const create_payment_entry = function (frm) {
	var d = new frappe.ui.Dialog({
		title: __("Select Mode of Payment"),
		fields: [
			{
				'fieldname': 'mode_of_payment',
				'fieldtype': 'Link',
				'label': __('Mode of Payment'),
				'options': 'Mode of Payment',
				"get_query": function () {
					return {
						filters: {
							type: ["in", ["Bank", "Cash"]]
						}
					};
				},
				'reqd': 1
			},
			{
				'fieldname': 'reference_no',
				'fieldtype': 'Data',
				'label': __('Número de referencia'),
			},
			{
				'fieldname': 'reference_date',
				'fieldtype': 'Date',
				'label': __('Fecha de referencia'),
			}
		],
	});
	d.set_primary_action(__('Create'), function() {
		d.hide();
		var arg = d.get_values();
		frappe.confirm(__("Creating Payment Entry. Do you want to proceed?"),
			function () {
				frappe.call({
					method: 'payout_entry',
					args: {
						"mode_of_payment": arg.mode_of_payment,
						"reference_no": arg.reference_no,
						"reference_date": arg.reference_date
					},
					callback: function () {
						frappe.set_route(
							'Form', "Payment Entry", {
								"Payment Entry Reference.reference_name": frm.doc.name
							}
						);
					},
					doc: frm.doc,
					freeze: true,
					freeze_message: __('Creating Payment Entry')
				});
			},
			function () {
				if (frappe.dom.freeze_count) {
					frappe.dom.unfreeze();
					frm.events.refresh(frm);
				}
			}
		);
	});
	d.show();
};

const create_additional_salary = function (frm) {
	frappe.confirm(__("Creating Additional Salary. Do you want to proceed?"),
		function () {
			frappe.call({
				method: 'payout_entry',
				args: {},
				callback: function () {
					frappe.set_route(
						"Form", "Additional Salary", {
							"Additional Salary.ref_docname": frm.doc.name
						}
					);
				},
				doc: frm.doc,
				freeze: true,
				freeze_message: __('Creating Additional Salary')
			});
		},
		function () {
			if (frappe.dom.freeze_count) {
				frappe.dom.unfreeze();
				frm.events.refresh(frm);
			}
		}
	);
};