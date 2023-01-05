frappe.listview_settings['Solicitud Cambios Proveedor'] = {	get_indicator: function (doc) {
		if (doc.status === "Pendiente") {
			return [__("Pendiente"), "grey", "status,=,Pendiente"];
		} else if (doc.status === "Aprobado") {
			return [__("Aprobado"), "green", "status,=,Aprobado"];
		} else if (doc.status === "Rechazado") {
			return [__("Rechazado"), "red", "status,=,Rechazado"];
		}
	},
};
