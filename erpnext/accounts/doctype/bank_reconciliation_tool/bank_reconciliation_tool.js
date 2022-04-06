// Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.provide("erpnext.accounts.bank_reconciliation");

frappe.ui.form.on("Bank Reconciliation Tool", {
	setup: function (frm) {
		frm.set_query("bank_account", function () {
			return {
				filters: {
					company: frm.doc.company,
					'is_company_account': 1
				},
			};
		});
	},

	refresh: function (frm) {
		frappe.require("assets/js/bank-reconciliation-tool.min.js", () =>
			frm.trigger("make_reconciliation_tool")
		);
		frm.upload_statement_button = frm.page.set_secondary_action(
			__("Upload Bank Statement"),
			() =>
				frappe.call({
					method:
						"erpnext.accounts.doctype.bank_statement_import.bank_statement_import.upload_bank_statement",
					args: {
						dt: frm.doc.doctype,
						dn: frm.doc.name,
						company: frm.doc.company,
						bank_account: frm.doc.bank_account,
					},
					callback: function (r) {
						if (!r.exc) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route(
								"Form",
								doc[0].doctype,
								doc[0].name
							);
						}
					},
				})
		);

		frm.conciliar_seleccionados_button = frm.page.add_button(
			"Conciliar seleccionados", 
			() => {
				var checked_indexes = frm.bank_reconciliation_data_table_manager.get_checked_indexes();
				var rows = frm.bank_reconciliation_data_table_manager.datatable.getRows();
				$.each(checked_indexes, function(i, idx) {
					var row = rows[idx];
					var payment_name = row[9].content;

					if (!payment_name) {
						return
					}

					var bank_transaction_name = $(row[11].content).attr("data-name");
					var payment_doctype = row[8].content;
					var amount = row[10].content;
					var vouchers = [{
						payment_doctype: payment_doctype,
						payment_name: payment_name,
						amount: amount,
					}]
					
					frappe.call({
						method: "erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.reconcile_vouchers",
						args: {
							bank_transaction_name: bank_transaction_name,
							vouchers: vouchers,
						},
						freeze: true,
						freeze_message: "Conciliando transacción bancaria",
						callback: (response) => {
							const alert_string = "Transacción bancaria " + bank_transaction_name + " conciliada";
							frappe.show_alert(alert_string);
						},
					});
				});
				cur_frm.refresh();
			}
		);
		frm.conciliar_seleccionados_button.hide();

		frm.eliminar_seleccionados_button = frm.page.add_button(
			"Eliminar seleccionados", 
			() => {
				var checked_indexes = frm.bank_reconciliation_data_table_manager.get_checked_indexes();
				var rows = frm.bank_reconciliation_data_table_manager.datatable.getRows();
				var bank_transaction_names = [];
				
				$.each(checked_indexes, function(i, idx) {
					var bank_transaction_name = $(rows[idx][11].content).attr("data-name");
					bank_transaction_names.push(bank_transaction_name);
				});
				
				frappe.call({
					method: "erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.delete_bank_transactions",
					args: {
						bank_transaction_names: bank_transaction_names,
					},
					freeze: true,
					freeze_message: "Eliminando transacciones bancarias",
					callback: (response) => {
						const alert_string = "Transacciones bancarias eliminadas";
						frappe.show_alert(alert_string);
						cur_frm.refresh();
					},
				});
			}
		);
		frm.eliminar_seleccionados_button.hide();

		frm.crear_asiento_button = frm.page.add_button(
			"Crear asientos", 
			() => {
				var checked_indexes = frm.bank_reconciliation_data_table_manager.get_checked_indexes();
				var rows = frm.bank_reconciliation_data_table_manager.datatable.getRows();
				var checked_rows_data = [];
				var dialog = new frappe.ui.Dialog({
					title: 'Detalles',
					fields: [
						{
							fieldname: 'second_account',
							fieldtype: 'Link',
							options: 'Account',
							reqd: 1,
							label: 'Cuenta',
							get_query: () => {
								return {
									filters: {
										is_group: 0,
										company: frm.doc.company,
									},
								};
							},
						},
						{
							fieldname: 'posting_date',
							fieldtype: 'Date',
							req: 1,
							label: 'Fecha de Referencia',
							default: frappe.datetime.get_today()
						}
					],
				});
				dialog.set_primary_action("Crear", () => {
					dialog.hide();
					$.each(checked_indexes, function(i, idx) {
						var row = rows[idx];
						var data = {
							bank_transaction_name: $(row[11].content).attr("data-name"),
							reference_date: row[2].content,
							reference_number: row[7].content,
							posting_date: dialog.fields_dict.posting_date.value,
							second_account: dialog.fields_dict.second_account.value,
							entry_type: "Journal Entry",
							mode_of_payment: "",
							cheque: "",
							party_type: "",
							party: "",
						}
						checked_rows_data.push(data);
					});

					frappe.call({
						method:"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.crear_asientos",
						args: {"data": checked_rows_data},
						freeze: true,
						freeze_message: "Creando asientos contables",
						callback: (response) => {
							const alert_string = "Transacciones bancarias añadidas como Asientos Contables";
							frappe.show_alert(alert_string);
							cur_frm.refresh();
						},
					});
				});
				dialog.show();
			}
		);
		frm.crear_asiento_button.hide();
	},

	after_save: function (frm) {
		frm.trigger("make_reconciliation_tool");
	},

	bank_account: function (frm) {
		frappe.db.get_value(
			"Bank Account",
			frm.bank_account,
			"account",
			(r) => {
				frappe.db.get_value(
					"Account",
					r.account,
					"account_currency",
					(r) => {
						frm.currency = r.account_currency;
					}
				);
			}
		);
		frm.trigger("get_account_opening_balance");
	},

	bank_statement_from_date: function (frm) {
		frm.trigger("get_account_opening_balance");
	},

	make_reconciliation_tool(frm) {
		frm.get_field("reconciliation_tool_cards").$wrapper.empty();
		if (frm.doc.bank_account && frm.doc.bank_statement_to_date) {
			frm.trigger("get_cleared_balance").then(() => {
				if (
					frm.doc.bank_account &&
					frm.doc.bank_statement_from_date &&
					frm.doc.bank_statement_to_date
				) {
					frm.trigger("render_chart");
					frm.trigger("render");
					frappe.utils.scroll_to(
						frm.get_field("reconciliation_tool_cards").$wrapper,
						true,
						30
					);
				}
			});
		}
	},

	get_account_opening_balance(frm) {
		if (frm.doc.bank_account && frm.doc.bank_statement_from_date) {
			frappe.call({
				method:
					"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_account_balance",
				args: {
					bank_account: frm.doc.bank_account,
					till_date: frm.doc.bank_statement_from_date,
				},
				callback: (response) => {
					frm.set_value("account_opening_balance", response.message);
				},
			});
		}
	},

	get_cleared_balance(frm) {
		if (frm.doc.bank_account && frm.doc.bank_statement_to_date) {
			return frappe.call({
				method:
					"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_account_balance",
				args: {
					bank_account: frm.doc.bank_account,
					till_date: frm.doc.bank_statement_to_date,
				},
				callback: (response) => {
					frm.cleared_balance = response.message;
				},
			});
		}
	},

	render_chart(frm) {
		frm.cards_manager = new erpnext.accounts.bank_reconciliation.NumberCardManager(
			{
				$reconciliation_tool_cards: frm.get_field(
					"reconciliation_tool_cards"
				).$wrapper,
				bank_statement_closing_balance:
					frm.doc.bank_statement_closing_balance,
				cleared_balance: frm.cleared_balance,
				currency: frm.currency,
			}
		);
	},

	render(frm) {
		if (frm.doc.bank_account) {
			frm.bank_reconciliation_data_table_manager = new erpnext.accounts.bank_reconciliation.DataTableManager(
				{
					company: frm.doc.company,
					bank_account: frm.doc.bank_account,
					$reconciliation_tool_dt: frm.get_field(
						"reconciliation_tool_dt"
					).$wrapper,
					$no_bank_transactions: frm.get_field(
						"no_bank_transactions"
					).$wrapper,
					bank_statement_from_date: frm.doc.bank_statement_from_date,
					bank_statement_to_date: frm.doc.bank_statement_to_date,
					bank_statement_closing_balance:
						frm.doc.bank_statement_closing_balance,
					cards_manager: frm.cards_manager,
				}
			);
		}
	},
});
