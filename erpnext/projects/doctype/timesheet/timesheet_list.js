frappe.listview_settings['Timesheet'] = {
	add_fields: ["status", "total_hours", "start_date", "end_date"],
	get_indicator: function(doc) {
		if (doc.status== "Billed") {
			return [__("Billed"), "green", "status,=," + "Billed"]
		}

		if (doc.status== "Payslip") {
			return [__("Payslip"), "green", "status,=," + "Payslip"]
		}

		if (doc.status== "Completed") {
			return [__("Completed"), "green", "status,=," + "Completed"]
		}
	},
	onload: function(listview) {
		var old_on_checked = listview.on_row_checked;

		listview.on_row_checked = function() {
			old_on_checked.apply(listview)

			listview.page.actions_btn_group.find(".user-action").remove();

			let checked_items = listview.get_checked_items();
			let customers = [];
			let status = [];

			for (i = 0; i < checked_items.length; i++) {
				if (!customers.includes(checked_items[i].customer)) {
					customers.push(checked_items[i].customer);
				}

				if (!status.includes(checked_items[i].status)) {
					status.push(checked_items[i].status);
				}
			}

			link_invoices(listview, customers, status);

		}
	}
};


function link_invoices(listview, customers, status) {
	const allEqual = arr => arr.every(val => val === arr[0]);

	if (frappe.user.has_role('Projects Manager') && allEqual(customers) && status.every(elem => ['Submitted'].includes(elem))) {
		
		listview.page.add_actions_menu_item("Vincular con factura", function() {
			let fields = [{
				"fieldtype": "Link",
				"label": __("Sales Invoice"),
				"fieldname": "sales_invoice",
				"options": "Sales Invoice",
				'reqd': 1,
				get_query: () => {
					var f = {
						docstatus: 1,
					}
					return {filters: f};
				},
			}];

			let dialog = new frappe.ui.Dialog({
				title: __("Vincular con Factura de Venta"),
				fields: fields
			});

			dialog.set_primary_action(__('Vincular'), () => {
				var args = dialog.get_values();
				if(!args) return;
				dialog.hide();
				return frappe.call({
					type: "GET",
					method: "erpnext.projects.doctype.timesheet.timesheet.link_sales_invoice",
					args: {
						"source_name": listview.get_checked_items(true),
						"sales_invoice": args.sales_invoice,
					},
					freeze: true,
					callback: function(r) {
						if(!r.exc) {
							frappe.model.sync(r.message);
							frappe.set_route("Form", r.message.doctype, r.message.name);
						}
					}
				});
			});
			dialog.show();
		});
	}
}
