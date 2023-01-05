// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Solicitud Cambios Proveedor', {
	refresh: function(frm) {
		if (frm.doc.status == 'Pendiente') {
			frm.add_custom_button("Aprobar", function() {
	            cambiar_estado(frm, "Aprobado")
	        }, __('Estado'));

	        frm.add_custom_button("Rechazar", function() {
	            cambiar_estado(frm, "Rechazado")
	        }, __('Estado'));
		}
	}
});

function cambiar_estado(frm, estado) {
	frappe.call({
        method: "erpnext.buying.doctype.solicitud_cambios_proveedor.solicitud_cambios_proveedor.cambiar_estado",
        args: { doctype: frm.doc.doctype, docname: frm.doc.name, estado: estado },
        callback: function(r, rt) {
            if (r.message) {
            	frm.reload_doc();
                frappe.msgprint({
                    title: 'Estado modificado',
                    indicator: 'green',
                    message: r.message,
                });
            }
        }
    });
}
