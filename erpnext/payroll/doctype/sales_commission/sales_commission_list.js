frappe.listview_settings['Sales Commission'] = {
	add_fields: ["total_commission_amount", "status"],
	get_indicator: function (doc) {
		if (doc.status == "Paid") {
			return [__(doc.status), "green", "status,=," + doc.status];
		}  else {
			return [__(doc.status), "red", "status,=," + doc.status];
		}
	},
	onload: function(listview){
		listview.page.add_actions_menu_item(__("Pagar Comisión"), function() {
			create_payment_entries();
		});
	}
};

const create_payment_entries = function () {
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
				cur_list.call_for_selected_items("erpnext.payroll.doctype.sales_commission.sales_commission.payout_entries", {
					"mode_of_payment": arg.mode_of_payment,
					"reference_no": arg.reference_no,
					"reference_date": arg.reference_date
				});
			},
			function () {
				if (frappe.dom.freeze_count) {
					frappe.dom.unfreeze();
				}
			}
		);
	});
	d.show();
};
