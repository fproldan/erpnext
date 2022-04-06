frappe.provide("erpnext.accounts.bank_reconciliation");

erpnext.accounts.bank_reconciliation.DataTableManager = class DataTableManager {
	constructor(opts) {
		Object.assign(this, opts);
		this.dialog_manager = new erpnext.accounts.bank_reconciliation.DialogManager(
			this.company,
			this.bank_account
		);
		this.make_dt();
	}

	make_dt() {
		var me = this;
		frappe.call({
			method: "erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_bank_transactions",
			args: {
				bank_account: this.bank_account,
			},
			reeze: true,
			freeze_message: "Obteniendo transacciones",
			callback: function (response) {
				me.format_data(response.message);
				me.get_dt_columns();
				me.get_datatable();
				me.set_listeners();
			},
		});
	}

	get_dt_columns() {
		this.columns = [
			{
				name: __("Date"),
				editable: false,
				width: 100,
			},
			{
				name: __("Description"),
				editable: false,
				width: 300,
			},
			{
				name: __("Deposit"),
				editable: false,
				width: 100,
				format: (value) =>
					"<span style='color:green;'>" +
					format_currency(value, this.currency) +
					"</span>",
			},
			{
				name: __("Withdrawal"),
				editable: false,
				width: 100,
				format: (value) =>
					"<span style='color:red;'>" +
					format_currency(value, this.currency) +
					"</span>",
			},
			{
				name: __("Unallocated Amount"),
				editable: false,
				width: 100,
				format: (value) =>
					"<span style='color:blue;'>" +
					format_currency(value, this.currency) +
					"</span>",
			},
			{
				name: __("Reference Number"),
				editable: false,
				width: 100,
			},
			{
				name: __("Tipo de Documento"),
				editable: false,
				width: 100,
			},
			{
				name: __("Documento"),
				editable: false,
				width: 180,
			},
			{
				name: __("Importe"),
				editable: false,
				width: 100,
				format: (value) => format_currency(value, this.currency) 
			},
			{
				name: __("Actions"),
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				width: 95,
			},
		];
	}

	format_data(transactions) {
		this.transactions = [];
		if (transactions[0]) {
			this.currency = transactions[0]["currency"];
		}
		this.transaction_dt_map = {};
		let length;
		transactions.forEach((row) => {
			length = this.transactions.push(this.format_row(row));
			this.transaction_dt_map[row["name"]] = length - 1;
		});
	}

	format_row(row) {
		if (row["linked_payment"]) {
			var matcheo_dt = row["linked_payment"][1];
			var matcheo_name = row["linked_payment"][2];
			var matcheo_amount = row["linked_payment"][3];
		} else {
			var matcheo_dt = null;
			var matcheo_name = null;
			var matcheo_amount = null;
		}
		return [
			row["date"],
			row["description"],
			row["deposit"],
			row["withdrawal"],
			row["unallocated_amount"],
			row["reference_number"],
			matcheo_dt,
			matcheo_name,
			matcheo_amount,
			`
			<Button class="btn btn-primary btn-xs center"  data-name = ${row["name"]} >
				Acciones
			</a>
			`,
		];
	}

	get_datatable() {
		var me = this;
		const datatable_options = {
			columns: this.columns,
			data: this.transactions,
			dynamicRowHeight: true,
			checkboxColumn: true,
			inlineFilters: true,
			events: {
				onCheckRow: function(data) {
					var checked_items = me.get_checked_indexes();
					if (checked_items.length) {
						cur_frm.conciliar_seleccionados_button.show();
						cur_frm.eliminar_seleccionados_button.show();
						cur_frm.crear_asiento_button.show();
					} else {
						cur_frm.conciliar_seleccionados_button.hide();
						cur_frm.eliminar_seleccionados_button.hide();
						cur_frm.crear_asiento_button.hide();
					}
				},
			}
		};
		this.datatable = new frappe.DataTable(
			this.$reconciliation_tool_dt.get(0),
			datatable_options
		);
		$(`.${this.datatable.style.scopeClass} .dt-scrollable`).css(
			"max-height",
			"calc(100vh - 400px)"
		);

		if (this.transactions.length > 0) {
			this.$reconciliation_tool_dt.show();
			this.$no_bank_transactions.hide();
		} else {
			this.$reconciliation_tool_dt.hide();
			this.$no_bank_transactions.show();
		}
	}

	get_checked_indexes() {
		var filtered_rows = this.datatable.datamanager.getFilteredRowIndices();
		var checked_rows = this.datatable.rowmanager.getCheckedRows();

		if (filtered_rows) {
			var filtered_rows = filtered_rows.map(function(e){return e.toString()});
			var filtered_and_checked = filtered_rows.filter(function(n) {
			    return checked_rows.indexOf(n) !== -1;
			});
			return filtered_and_checked
		}

		return checked_rows
	}

	set_listeners() {
		var me = this;
		$(`.${this.datatable.style.scopeClass} .dt-scrollable`).on(
			"click",
			`.btn`,
			function () {
				me.dialog_manager.show_dialog(
					$(this).attr("data-name"),
					(bank_transaction) => me.update_dt_cards(bank_transaction)
				);
				return true;
			}
		);
	}

	update_dt_cards(bank_transaction) {
		const transaction_index = this.transaction_dt_map[
			bank_transaction.name
		];
		if (bank_transaction.unallocated_amount > 0) {
			this.transactions[transaction_index] = this.format_row(
				bank_transaction
			);
		} else {
			this.transactions.splice(transaction_index, 1);
		}
		this.datatable.refresh(this.transactions, this.columns);

		if (this.transactions.length == 0) {
			this.$reconciliation_tool_dt.hide();
			this.$no_bank_transactions.show();
		}

		// this.make_dt();
		this.get_cleared_balance().then(() => {
			this.cards_manager.$cards[1].set_value(
				format_currency(this.cleared_balance),
				this.currency
			);
			this.cards_manager.$cards[2].set_value(
				format_currency(
					this.bank_statement_closing_balance - this.cleared_balance
				),
				this.currency
			);
			this.cards_manager.$cards[2].set_value_color(
				this.bank_statement_closing_balance - this.cleared_balance == 0
					? "text-success"
					: "text-danger"
			);
		});
	}

	get_cleared_balance() {
		if (this.bank_account && this.bank_statement_to_date) {
			return frappe.call({
				method:
					"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_account_balance",
				args: {
					bank_account: this.bank_account,
					till_date: this.bank_statement_to_date,
				},
				callback: (response) =>
					(this.cleared_balance = response.message),
			});
		}
	}
};
