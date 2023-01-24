frappe.pages['consulta-cuit'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Consulta de CUIT',
		single_column: true
	});

	new erpnext.ConsultaCuit(page);
}

erpnext.ConsultaCuit = class ConsultaCuit {
	constructor(page) {
		this.page = page;
		this.make_form();
	}

	make_form() {
		this.form = new frappe.ui.FieldGroup({
			fields: [
				{
					label: __('CUIT'),
					fieldname: 'tax_id',
					fieldtype: 'Data',
					change: () => this.fetch_and_render(),
				},
				{
					fieldtype: 'Section Break'
				},
				{
					fieldtype: 'HTML',
					fieldname: 'preview'
				}
			],
			body: this.page.body
		});
		this.form.make();
	}

	fetch_and_render() {
		let values = this.form.get_values();
		
		// set working state
		this.form.get_field('preview').html(`
			<div class="text-muted margin-top">
				${__("Fetching...")}
			</div>
		`);

		frappe.call('erpnext.crm.utils.get_cuit', {tax_id: values['tax_id']}).then(r => {
			let cuit_values = r.message;

			this.render(cuit_values);

			let me = this;
			this.page.clear_inner_toolbar();

			if (!cuit_values['customer']) {
				this.page.add_inner_button(__('Crear cliente'), function() {
					me.crear_cliente(cuit_values);
				});
			}

			if (!cuit_values['lead']) {
				this.page.add_inner_button(__('Crear iniciativa'), function() {
					me.crear_iniciativa(cuit_values);
				});
			}

			console.log(cuit_values)
			if (cuit_values['lead'] && !cuit_values['lead']['assign']) {
				this.page.add_inner_button(__('Autoasignar'), function() {
					me.autoasignar(cuit_values);
				});
			}
		});
	}

	crear_entidad(doctype, tax_id) {
		return frappe.call({
			type: "GET",
			method: "erpnext.crm.utils.crear_entidad",
			args: {
				"doctype": doctype,
				"tax_id": tax_id,
			},
			freeze: true,
			callback: function(r) {
				if(!r.exc) {
					frappe.model.sync(r.message);
					frappe.set_route("Form", r.message.doctype, r.message.name);
				}
			}
		});
	}

	crear_cliente(cuit_values) {
		let values = this.form.get_values();
		this.crear_entidad('Customer', values['tax_id']);
	}

	crear_iniciativa(cuit_values) {
		let values = this.form.get_values();
		this.crear_entidad('Lead', values['tax_id']);
	}

	autoasignar(cuit_values) {
		let values = this.form.get_values();
		frappe.call({
			type: "GET",
			method: "erpnext.crm.utils.autoasignar",
			args: {
				"name": cuit_values['lead']['base_name'],
				"user": frappe.user.name,
			},
			freeze: true,
			callback: function(r) {
				if(!r.exc) {
					frappe.msgprint(r.message)
				}
			}
		});
	}

	render(cuit_values) {
		let customer_html = '';
		let lead_html = '';

		let estado_cuenta = `
		 	<div class="row">
                <div class="col-lg-12 d-flex align-items-stretch">
                    <div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                        <h5 class="border-bottom pb-2">Estado de Cuenta</h5>
                        <div id="shopify-product-list">
                            <h4 class="text-center ${cuit_values['estado_cuit_class']}" style="margin-bottom: 0px;">${cuit_values['estado_cuit']}</h4>
                        </div>
                    </div>
                </div>
            </div>
		`
		if (cuit_values['customer']) {
			customer_html = `
				<div class="row">
                	<div class="col-lg-12 d-flex align-items-stretch">
                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                    		<h5 class="border-bottom pb-2">Cliente</h5>
							<div>
								<table class="table table-bordered">
									<tr>
										<th width="33%">Razon Social</th>
										<th width="33%">Cliente</th>
									</tr>
									<tr>
										<td>${cuit_values['customer']['customer_name']}</td>
										<td>${cuit_values['customer']['name']}</td>
									</tr>
								</table>
							</div>
						</div>
					</div>
				</div>
			`;
		} else {
			customer_html = `
				<div class="row">
                	<div class="col-lg-12 d-flex align-items-stretch">
                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                    		<h5 class="border-bottom pb-2">Cliente</h5>
							<h5 class="text-muted">No hay Cliente con ese CUIT</h5>
						</div>
					</div>
				</div>
			`
		}

		if (cuit_values['lead']) {
			lead_html = `
				<div class="row">
                	<div class="col-lg-12 d-flex align-items-stretch">
                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                    		<h5 class="border-bottom pb-2">Iniciativa</h5>
							<div>
								<table class="table table-bordered">
									<tr>
										<th width="33%">Razon Social</th>
										<th width="33%">Iniciativa</th>
										<th width="33%">Asignado</th>
									</tr>
									<tr>
										<td>${cuit_values['lead']['lead_name']}</td>
										<td>${cuit_values['lead']['name']}</td>
										<td>${cuit_values['lead']['assign']}</td>
									</tr>
								</table>
							</div>
						</div>
					</div>
				</div>
			`;
		} else {
			lead_html = `
				<div class="row">
                	<div class="col-lg-12 d-flex align-items-stretch">
                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                    		<h5 class="border-bottom pb-2">Iniciativa</h5>
							<h5 class="text-muted">No hay Iniciativa con ese CUIT</h5>
						</div>
					</div>
				</div>
			`
		}

		let html = `
			${estado_cuenta}
			${customer_html}
			${lead_html}
		`;

		this.form.get_field('preview').html(html);
	}
	
};
