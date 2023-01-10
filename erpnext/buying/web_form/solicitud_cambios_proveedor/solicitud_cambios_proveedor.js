frappe.ready(function() {
	frappe.web_form.after_load = () => {
		frappe.web_form.set_value('proveedor', '{{ supplier }}');
		frappe.web_form.set_value('usuario', '{{ usuario }}');
		frappe.web_form.set_df_property('proveedor', 'hidden', 1);
		frappe.web_form.set_df_property('usuario', 'hidden', 1);
		frappe.web_form.fields_dict.proveedor.refresh();
		frappe.web_form.fields_dict.usuario.refresh();

		if ('{{ status }}' != 'Pendiente') {
			frappe.web_form.set_df_property('nota', 'read_only', 1);
			frappe.web_form.set_df_property('archivo', 'read_only', 1);
			$('.btn-primary').hide();
		}

		
	}
})
