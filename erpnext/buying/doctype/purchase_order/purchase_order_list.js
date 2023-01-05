frappe.listview_settings['Purchase Order'] = {
	add_fields: ["base_grand_total", "company", "currency", "supplier",
		"supplier_name", "per_received", "per_billed", "status"],
	get_indicator: function (doc) {
		if (doc.status === "Closed") {
			return [__("Closed"), "green", "status,=,Closed|aprobado_por_proveedor,==,1"];
		} else if (doc.status === "On Hold") {
			return [__("On Hold"), "orange", "status,=,On Hold|aprobado_por_proveedor,==,1"];
		} else if (doc.status === "Delivered") {
			return [__("Delivered"), "green", "status,=,Closed|aprobado_por_proveedor,==,1"];
		} else if (doc.status === "Pendiente de Confirmacion") {
			return [__("Pendiente de Confirmacion"), "grey", "status,=,Pendiente de Confirmacion"];
		} else if (flt(doc.per_received, 2) < 100 && doc.status !== "Closed") {
			if (flt(doc.per_billed, 2) < 100) {
				return [__("To Receive and Bill"), "orange", "per_received,<,100|per_billed,<,100|status,!=,Closed|aprobado_por_proveedor,==,1"];
			} else {
				return [__("To Receive"), "orange", "per_received,<,100|per_billed,=,100|status,!=,Closed|aprobado_por_proveedor,==,1"];
			}
		} else if (flt(doc.per_received, 2) >= 100 && flt(doc.per_billed, 2) < 100 && doc.status !== "Closed") {
			return [__("To Bill"), "orange", "per_received,=,100|per_billed,<,100|status,!=,Closed|aprobado_por_proveedor,==,1"];
		} else if (flt(doc.per_received, 2) >= 100 && flt(doc.per_billed, 2) == 100 && doc.status !== "Closed") {
			return [__("Completed"), "green", "per_received,=,100|per_billed,=,100|status,!=,Closed|aprobado_por_proveedor,==,1"];
		}
	},
	onload: function (listview) {
		var method = "erpnext.buying.doctype.purchase_order.purchase_order.close_or_unclose_purchase_orders";

		listview.page.add_menu_item(__("Close"), function () {
			listview.call_for_selected_items(method, { "status": "Closed" });
		});

		listview.page.add_menu_item(__("Re-open"), function () {
			listview.call_for_selected_items(method, { "status": "Submitted" });
		});
	}
};
