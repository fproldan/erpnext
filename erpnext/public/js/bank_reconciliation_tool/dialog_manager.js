frappe.provide("erpnext.accounts.bank_reconciliation");

erpnext.accounts.bank_reconciliation.DialogManager = class DialogManager {
	constructor(company, bank_account) {
		this.bank_account = bank_account;
		this.company = company;
		this.make_dialog();
	}

	show_dialog(bank_transaction_name, update_dt_cards) {
		this.bank_transaction_name = bank_transaction_name;
		this.update_dt_cards = update_dt_cards;
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "Bank Transaction",
				filters: { name: this.bank_transaction_name },
				fieldname: [
					"date",
					"deposit",
					"withdrawal",
					"currency",
					"description",
					"name",
					"bank_account",
					"company",
					"reference_number",
					"party_type",
					"party",
					"unallocated_amount",
					"allocated_amount",
				],
			},
			callback: (r) => {
				if (r.message) {
					this.bank_transaction = r.message;
					r.message.payment_entry = 1;
					this.dialog.set_values(r.message);
					this.dialog.show();
				}
			},
		});
	}

	get_linked_vouchers(document_types) {
		frappe.call({
			method:
				"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_linked_payments",
			args: {
				bank_transaction_name: this.bank_transaction_name,
				document_types: document_types,
			},

			callback: (result) => {
				const data = result.message;

				if (data && data.length > 0) {
					const proposals_wrapper = this.dialog.fields_dict.payment_proposals.$wrapper;
					proposals_wrapper.show();
					this.dialog.fields_dict.no_matching_vouchers.$wrapper.hide();
					this.data = [];
					data.forEach((row) => {
						const reference_date = row[5] ? row[5] : row[8];
						this.data.push([
							__(row[1]),
							row[2],
							reference_date,
							format_currency(row[3], row[9]),
							row[6],
							row[4],
							row[1],
						]);
					});
					this.get_dt_columns();
					this.get_datatable(proposals_wrapper);
				} else {
					const proposals_wrapper = this.dialog.fields_dict.payment_proposals.$wrapper;
					proposals_wrapper.hide();
					this.dialog.fields_dict.no_matching_vouchers.$wrapper.show();

				}
				this.dialog.show();
			},
		});
	}

	get_dt_columns() {
		this.columns = [
			{
				name: __("Document Type"),
				editable: false,
				width: 150,
			},
			{
				name: __("Document Name"),
				editable: false,
				width: 180,
			},
			{
				name: __("Reference Date"),
				editable: false,
				width: 120,
			},
			{
				name: __("Amount"),
				editable: false,
				width: 100,
			},
			{
				name: __("Party"),
				editable: false,
				width: 120,
			},
			{
				name: __("Reference Number"),
				editable: false,
				width: 140,
			},
			{
				name: __("DocType"),
				editable: false,
				width: 80,
			},
		];
	}

	get_datatable(proposals_wrapper) {
		if (!this.datatable) {
			const datatable_options = {
				columns: this.columns,
				data: this.data,
				dynamicRowHeight: true,
				checkboxColumn: true,
				inlineFilters: true,
			};
			this.datatable = new frappe.DataTable(
				proposals_wrapper.get(0),
				datatable_options
			);
		} else {
			this.datatable.refresh(this.data, this.columns);
			this.datatable.rowmanager.checkMap = [];
		}
	}

	make_dialog() {
		const me = this;
		me.selected_payment = null;
		const fields = [
			{
				label: __("Action"),
				fieldname: "action",
				fieldtype: "Select",
				options: `Conciliar con comprobante\nCrear comprobante\nActualizar transacción bancaria`,
				default: "Conciliar con comprobante",
			},
			{
				fieldname: "column_break_4",
				fieldtype: "Column Break",
			},
			{
				label: __("Document Type"),
				fieldname: "document_type",
				fieldtype: "Select",
				options: `Payment Entry\nJournal Entry`,
				default: "Payment Entry",
				depends_on: "eval:doc.action=='Crear comprobante'",
			},
			{
				fieldtype: "Section Break",
				fieldname: "section_break_1",
				label: __("Filters"),
				depends_on: "eval:doc.action=='Conciliar con comprobante'",
			},
			{
				fieldtype: "Check",
				label: __("Payment Entry"),
				fieldname: "payment_entry",
				onchange: () => this.update_options(),
			},
			{
				fieldtype: "Check",
				label: __("Journal Entry"),
				fieldname: "journal_entry",
				onchange: () => this.update_options(),
			},
			{
				fieldname: "column_break_5",
				fieldtype: "Column Break",
			},
			{
				fieldtype: "Check",
				label: __("Sales Invoice"),
				fieldname: "sales_invoice",
				onchange: () => this.update_options(),
			},

			{
				fieldtype: "Check",
				label: __("Purchase Invoice"),
				fieldname: "purchase_invoice",
				onchange: () => this.update_options(),
			},
			{
				fieldname: "column_break_5",
				fieldtype: "Column Break",
			},
			{
				fieldtype: "Check",
				label: __("Expense Claim"),
				fieldname: "expense_claim",
				onchange: () => this.update_options(),
			},
			{
				fieldtype: "Check",
				label: __("Show Only Exact Amount"),
				fieldname: "exact_match",
				default: 1,
				onchange: () => this.update_options(),
			},
			{
				fieldtype: "Section Break",
				fieldname: "section_break_1",
				label: __("Select Vouchers to Match"),
				depends_on: "eval:doc.action=='Conciliar con comprobante'",
			},
			{
				fieldtype: "HTML",
				fieldname: "payment_proposals",
			},
			{
				fieldtype: "HTML",
				fieldname: "no_matching_vouchers",
				options: __("<div class='text-muted text-center'>No Matching Vouchers Found</div>")
			},
			{
				fieldtype: "Section Break",
				fieldname: "details",
				label: __("Details"),
				depends_on: "eval:doc.action!='Conciliar con comprobante'",
			},
			{
				label: "Cheque",
				fieldname: "cheque",
				fieldtype: "Link",
				options: "Cheque",
				depends_on: "eval:doc.action=='Crear comprobante' && doc.document_type=='Journal Entry' && (doc.journal_entry_type=='Cheque Depositado' || doc.journal_entry_type=='Cheque Rechazado' || doc.journal_entry_type=='Cheque Cobrado' || doc.journal_entry_type=='Cheque Debitado')",
				get_query: () => {
					var journal_entry_type = this.dialog.fields_dict.journal_entry_type.value;
					
					if (journal_entry_type == 'Cheque Depositado') {
						var estados = ['En Mano'];
					} else if (journal_entry_type == 'Cheque Cobrado') {
						var estados = ['En Mano', 'Vencido'];
					} else if (journal_entry_type == 'Cheque Rechazado') {
						var estados = ['Vencido', 'Depositado', 'Entregado', 'Cobrado'];
					} else if (journal_entry_type == 'Cheque Debitado') {
						var estados = ['Entregado'];
					}

					return {
						filters: [["estado", "in", estados]]
					};
				},
			},
			{
				fieldname: "reference_number",
				fieldtype: "Data",
				label: __("Reference Number"),
				mandatory_depends_on: "eval:doc.action=='Crear comprobante' && !(doc.journal_entry_type=='Cheque Depositado' || doc.journal_entry_type=='Cheque Rechazado' || doc.journal_entry_type=='Cheque Cobrado' || doc.journal_entry_type=='Cheque Debitado')",
			},
			{
				default: "Today",
				fieldname: "posting_date",
				fieldtype: "Date",
				label: __("Posting Date"),
				reqd: 1,
				depends_on: "eval:doc.action=='Crear comprobante'",
			},
			{
				fieldname: "reference_date",
				fieldtype: "Date",
				label: __("Cheque/Reference Date"),
				mandatory_depends_on: "eval:doc.action=='Crear comprobante' && !(doc.journal_entry_type=='Cheque Depositado' || doc.journal_entry_type=='Cheque Rechazado' || doc.journal_entry_type=='Cheque Cobrado' || doc.journal_entry_type=='Cheque Debitado')",
				depends_on: "eval:doc.action=='Crear comprobante'",
				reqd: 1,
			},
			{
				fieldname: "mode_of_payment",
				fieldtype: "Link",
				label: __("Mode of Payment"),
				options: "Mode of Payment",
				depends_on: "eval:doc.action=='Crear comprobante'",
			},
			{
				fieldname: "edit_in_full_page",
				fieldtype: "Button",
				label: __("Edit in Full Page"),
				click: () => {
					this.edit_in_full_page();
				},
				depends_on:
					"eval:doc.action=='Crear comprobante'",
			},
			{
				fieldname: "column_break_7",
				fieldtype: "Column Break",
			},
			{
				default: "Journal Entry Type",
				fieldname: "journal_entry_type",
				fieldtype: "Select",
				label: __("Journal Entry Type"),
				options:
					"Journal Entry\nInter Company Journal Entry\nBank Entry\nCash Entry\nCredit Card Entry\nDebit Note\nCredit Note\nContra Entry\nExcise Entry\nWrite Off Entry\nOpening Entry\nDepreciation Entry\nExchange Rate Revaluation\nDeferred Revenue\nDeferred Expense\nAjuste por Inflacion\nCheque Rechazado\nCheque Depositado\nCheque Cobrado\nCheque Debitado",
				depends_on:
					"eval:doc.action=='Crear comprobante' &&  doc.document_type=='Journal Entry'",
				mandatory_depends_on:
					"eval:doc.action=='Crear comprobante' &&  doc.document_type=='Journal Entry'",
				onchange: () => this.clean_cheque_add_account(),
			},
			{
				fieldname: "second_account",
				fieldtype: "Link",
				label: __("Account"),
				options: "Account",
				depends_on:
					"eval:doc.action=='Crear comprobante' &&  doc.document_type=='Journal Entry'",
				mandatory_depends_on:
					"eval:doc.action=='Crear comprobante' &&  doc.document_type=='Journal Entry'",
				get_query: () => {
					return {
						filters: {
							is_group: 0,
							company: this.company,
						},
					};
				},
			},
			{
				fieldname: "party_type",
				fieldtype: "Link",
				label: __("Party Type"),
				options: "DocType",
				mandatory_depends_on:
				"eval:doc.action=='Crear comprobante' &&  doc.document_type=='Payment Entry'",
				get_query: function () {
					return {
						filters: {
							name: [
								"in",
								Object.keys(frappe.boot.party_account_types),
							],
						},
					};
				},
			},
			{
				fieldname: "party",
				fieldtype: "Dynamic Link",
				label: __("Party"),
				options: "party_type",
				mandatory_depends_on:
					"eval:doc.action=='Crear comprobante' && doc.document_type=='Payment Entry'",
			},
			{
				fieldname: "project",
				fieldtype: "Link",
				label: __("Project"),
				options: "Project",
				depends_on:
					"eval:doc.action=='Crear comprobante' && doc.document_type=='Payment Entry'",
			},
			{
				fieldname: "cost_center",
				fieldtype: "Link",
				label: __("Cost Center"),
				options: "Cost Center",
				depends_on:
					"eval:doc.action=='Crear comprobante' && doc.document_type=='Payment Entry'",
			},
			{
				fieldtype: "Section Break",
				fieldname: "details_section",
				label: __("Transaction Details"),
				collapsible: 1,
			},
			{
				fieldname: "deposit",
				fieldtype: "Currency",
				label: __("Deposit"),
				read_only: 1,
			},
			{
				fieldname: "withdrawal",
				fieldtype: "Currency",
				label: __("Withdrawal"),
				read_only: 1,
			},
			{
				fieldname: "description",
				fieldtype: "Small Text",
				label: __("Description"),
				read_only: 1,
			},
			{
				fieldname: "column_break_17",
				fieldtype: "Column Break",
				read_only: 1,
			},
			{
				fieldname: "allocated_amount",
				fieldtype: "Currency",
				label: __("Allocated Amount"),
				read_only: 1,
			},

			{
				fieldname: "unallocated_amount",
				fieldtype: "Currency",
				label: __("Unallocated Amount"),
				read_only: 1,
			},
		];

		me.dialog = new frappe.ui.Dialog({
			title: __("Reconcile the Bank Transaction"),
			fields: fields,
			size: "large",
			primary_action: (values) =>
				this.reconciliation_dialog_primary_action(values),
		});
	}

	get_selected_attributes() {
		let selected_attributes = [];
		this.dialog.$wrapper.find(".checkbox input").each((i, col) => {
			if ($(col).is(":checked")) {
				selected_attributes.push($(col).attr("data-fieldname"));
			}
		});

		return selected_attributes;
	}

	update_options() {
		let selected_attributes = this.get_selected_attributes();
		this.get_linked_vouchers(selected_attributes);
	}

	clean_cheque_add_account() {
		var me = this;
		
		me.dialog.fields_dict.cheque.value = null;
		me.dialog.get_field("cheque").refresh();

		var journal_entry_type = me.dialog.fields_dict.journal_entry_type.input.value;

		if (journal_entry_type == 'Cheque Depositado' || journal_entry_type == 'Cheque Cobrado' || journal_entry_type == 'Cheque Rechazado' || journal_entry_type == 'Cheque Debitado')  {
			frappe.call({
		    	method:"erpnext_argentina.cheques.get_cuentas_cheque",
			    args: {
			    	company: me.company
			   	}, 
			    callback: function(r) {
			        if (r.message) {
			        	if (journal_entry_type == 'Cheque Depositado') {
			        		var cuenta = r.message["cuenta_depositos"];
			        	} else if (journal_entry_type == 'Cheque Cobrado') {
			                var cuenta = r.message["cuenta_cobros"];
			            } else if (journal_entry_type == 'Cheque Rechazado') {
			        		var cuenta = r.message["cuenta_rechazados"];
			        	}
			        	me.dialog.fields_dict.second_account.value = cuenta;
						me.dialog.get_field("second_account").refresh();
					}
				}
			});
		}
	}

	reconciliation_dialog_primary_action(values) {
		if (values.action == "Conciliar con comprobante") this.match(values);
		if (
			values.action == "Crear comprobante" &&
			values.document_type == "Payment Entry"
		)
			this.add_payment_entry(values);
		if (
			values.action == "Crear comprobante" &&
			values.document_type == "Journal Entry"
		)
			this.add_journal_entry(values);
		else if (values.action == "Actualizar transacción bancaria")
			this.update_transaction(values);
	}

	match() {
		var selected_map = this.datatable.rowmanager.checkMap;
		let rows = [];
		selected_map.forEach((val, index) => {
			if (val == 1) rows.push(this.datatable.datamanager.rows[index]);
		});
		let vouchers = [];
		rows.forEach((x) => {
			vouchers.push({
				payment_doctype: x[8].content,
				payment_name: x[3].content,
				amount: x[5].content,
			});
		});
		frappe.call({
			method:
				"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.reconcile_vouchers",
			args: {
				bank_transaction_name: this.bank_transaction.name,
				vouchers: vouchers,
			},
			callback: (response) => {
				const alert_string = "Transacción bancaria " + this.bank_transaction.name + " conciliada";
				frappe.show_alert(alert_string);
				this.update_dt_cards(response.message);
				this.dialog.hide();
				console.log('2222');
				cur_page.page.frm.refresh();
			},
		});
	}

	add_payment_entry(values) {
		frappe.call({
			method:
				"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.create_payment_entry_bts",
			args: {
				bank_transaction_name: this.bank_transaction.name,
				reference_number: values.reference_number,
				reference_date: values.reference_date,
				party_type: values.party_type,
				party: values.party,
				posting_date: values.posting_date,
				mode_of_payment: values.mode_of_payment,
				project: values.project,
				cost_center: values.cost_center,
			},
			callback: (response) => {
				const alert_string = "Transacción bancaria " + this.bank_transaction.name + " añadida como Entrada de Pago";
				frappe.show_alert(alert_string);
				this.update_dt_cards(response.message);
				this.dialog.hide();
				console.log('2222');
				cur_page.page.frm.refresh();
			},
		});
	}

	add_journal_entry(values) {
		frappe.call({
			method:
				"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.create_journal_entry_bts",
			args: {
				bank_transaction_name: this.bank_transaction.name,
				reference_number: values.reference_number,
				reference_date: values.reference_date,
				party_type: values.party_type,
				party: values.party,
				posting_date: values.posting_date,
				mode_of_payment: values.mode_of_payment,
				entry_type: values.journal_entry_type,
				second_account: values.second_account,
				cheque: values.cheque,
			},
			callback: (response) => {
				const alert_string = "Transacción bancaria " + this.bank_transaction.name + " añadida como Asiento Contable";
				frappe.show_alert(alert_string);
				this.update_dt_cards(response.message);
				this.dialog.hide();
				console.log('2222');
				cur_page.page.frm.refresh();
			},
		});
	}

	update_transaction(values) {
		frappe.call({
			method:
				"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.update_bank_transaction",
			args: {
				bank_transaction_name: this.bank_transaction.name,
				reference_number: values.reference_number,
				party_type: values.party_type,
				party: values.party,
			},
			callback: (response) => {
				const alert_string = "Transacción bancaria " + this.bank_transaction.name + " editada";
				frappe.show_alert(alert_string);
				this.update_dt_cards(response.message);
				this.dialog.hide();
			},
		});
	}

	edit_in_full_page() {
		const values = this.dialog.get_values(true);
		if (values.document_type == "Payment Entry") {
			frappe.call({
				method:
					"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.create_payment_entry_bts",
				args: {
					bank_transaction_name: this.bank_transaction.name,
					reference_number: values.reference_number,
					reference_date: values.reference_date,
					party_type: values.party_type,
					party: values.party,
					posting_date: values.posting_date,
					mode_of_payment: values.mode_of_payment,
					project: values.project,
					cost_center: values.cost_center,
					allow_edit: true
				},
				callback: (r) => {
					const doc = frappe.model.sync(r.message);
					frappe.set_route("Form", doc[0].doctype, doc[0].name);
				},
			});
		} else {
			frappe.call({
				method:
					"erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.create_journal_entry_bts",
				args: {
					bank_transaction_name: this.bank_transaction.name,
					reference_number: values.reference_number,
					reference_date: values.reference_date,
					party_type: values.party_type,
					party: values.party,
					posting_date: values.posting_date,
					mode_of_payment: values.mode_of_payment,
					entry_type: values.journal_entry_type,
					second_account: values.second_account,
					cheque: values.cheque,
					allow_edit: true
				},
				callback: (r) => {
					var doc = frappe.model.sync(r.message);
					frappe.set_route("Form", doc[0].doctype, doc[0].name);
				},
			});
		}
	}

};
