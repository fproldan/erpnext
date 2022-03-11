frappe.provide('frappe.ui.form');

frappe.ui.form.SupplierQuickEntryForm = class SupplierQuickEntryForm extends frappe.ui.form.QuickEntryForm {
	constructor(doctype, after_insert, init_callback, doc, force) {
		super(doctype, after_insert, init_callback, doc, force);
		this.skip_redirect_on_error = true;
	}

	render_dialog() {
		// Set tax_id in second place
		var tax_id = this.mandatory.splice(2, 1);
		this.mandatory.splice(1, 0, tax_id[0]);

		this.mandatory = this.mandatory.concat(this.get_variant_fields());
		super.render_dialog();
	}

	get_variant_fields() {
		var variant_fields = [
			{
				fieldtype: "Section Break",
				label: __("Primary Contact Details"),
				collapsible: 1
			},
			{
				label: __("Email Id"),
				fieldname: "email_id",
				fieldtype: "Data"
			},
			{
				fieldtype: "Column Break"
			},
			{
				label: __("Mobile Number"),
				fieldname: "mobile_no",
				fieldtype: "Data"
			},
			{
				fieldtype: "Section Break",
				label: __("Primary Address Details"),
				collapsible: 1
			},
			{
				label: __("Address Line 1"),
				fieldname: "address_line1",
				fieldtype: "Data"
			},
			{
				label: __("Address Line 2"),
				fieldname: "address_line2",
				fieldtype: "Data"
			},
			{
				label: __("ZIP Code"),
				fieldname: "pincode",
				fieldtype: "Data"
			},
			{
				fieldtype: "Column Break"
			},
			{
				label: __("City"),
				fieldname: "city",
				fieldtype: "Data"
			},
			{
				label: __("Jurisdicción"),
				fieldname: "jurisdiccion",
				fieldtype: "Link",
				options: "Jurisdiccion"
			},
			{
				label: __("Country"),
				fieldname: "country",
				fieldtype: "Link",
				options: "Country"
			}
		];

		return variant_fields;
	}
};
