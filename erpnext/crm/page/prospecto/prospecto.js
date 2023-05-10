frappe.pages['prospecto'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Prospecto',
		single_column: true
	});
	new erpnext.Prospecto(page);
}

erpnext.Prospecto = class Prospecto {
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
					fieldtype: 'Column Break'
				},
				{
					label: __('Razón Social'),
					fieldname: 'customer_name',
					fieldtype: 'Link',
					options: 'Customer',
					only_select: true,
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
		
		this.form.get_field('preview').html(`
			<h5 class="text-muted margin-top">
				${__("Fetching...")}
			</h5>
		`);

		if (!values['tax_id'] && !values['customer_name']) {
			return
		}

		frappe.call('erpnext.crm.utils.get_cuit', {tax_id: values['tax_id'], customer_name: values['customer_name']}).then(r => {
			let cuit_values = r.message;

			this.render(cuit_values);

			let me = this;
			this.page.clear_inner_toolbar();

			this.page.add_button(__('Condiciones comerciales'), function() {
				console.log('')
			}, {btn_class: 'btn-primary'});

			if (cuit_values['estado_cuit'] != 'Inhabilitado') {
				this.page.add_inner_button(__('Verificar estado NOSIS'), function() {
					me.verificar_nosis(cuit_values);
				}, __('Acciones'));
			}
			
			if (cuit_values['estado_cuit'] != 'Inhabilitado') {
				this.page.set_inner_btn_group_as_primary(__('Acciones'));
			}
			if (cuit_values['lead'] && me.se_puede_mostrar(cuit_values)) {
				this.page.set_inner_btn_group_as_primary(__('Tarea'));
			}

			if (!cuit_values['customer']) {
				this.page.add_inner_button(__('Crear prospecto'), function() {
					me.crear_cliente(cuit_values);
				}, __('Acciones'));
			}

			if (!cuit_values['lead'] && cuit_values['estado_cuit'] != 'Inhabilitado') {
				this.page.add_inner_button(__('Crear iniciativa'), function() {
					me.crear_iniciativa(cuit_values);
				}, __('Acciones'));
			}

			if (cuit_values['lead'] && me.se_puede_mostrar(cuit_values)) {
				this.page.add_inner_button(__('Crear cotización desde inciativa'), function() {
					me.crear_cotizacion_iniciativa(cuit_values);
				}, __('Acciones'));
			}

			if (cuit_values['customer'] && cuit_values['estado_cuit'] != 'Inhabilitado' && me.se_puede_mostrar(cuit_values)) {
				this.page.add_inner_button(__('Crear cotización desde cliente'), function() {
					me.crear_cotizacion_cliente(cuit_values);
				}, __('Acciones'));
			}

			if (cuit_values['lead'] && !cuit_values['lead']['assign']) {
				this.page.add_inner_button(__('Autoasignar'), function() {
					me.autoasignar(cuit_values);
				}, __('Acciones'));
			}

			if (cuit_values['lead'] && me.se_puede_mostrar(cuit_values)) {
				let create_event = () => {
					const args = {
						doc: cuit_values['lead']['base_name'],
						reference_doctype: 'Lead',
						reference_document: cuit_values['lead']['base_name'],
					};
					return new frappe.views.InteractionComposer(args);
				};

				this.page.add_inner_button(__('Evento'), function() {
					create_event('calendar');
					me.fetch_and_render();
				}, __('Tarea'), 'primary');
			}
		});
	}

	verificar_nosis(cuit_values) {

	}

	crear_entidad(doctype, tax_id, customer_name) {
		return frappe.call({
			type: "GET",
			method: "erpnext.crm.utils.crear_entidad",
			args: {"doctype": doctype, "tax_id": tax_id, "customer_name": customer_name},
			freeze: true,
			callback: function(r) {
				if(!r.exc) {
					frappe.model.sync(r.message);
					frappe.set_route("Form", r.message.doctype, r.message.name);
				}
			}
		});
	}

	crear_cotizacion(quotation_to, party_name) {
		return frappe.call({
			type: "GET",
			method: "erpnext.crm.utils.crear_cotizacion",
			args: {
				"quotation_to": quotation_to,
				"party_name": party_name ,
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
		this.crear_entidad('Customer', values['tax_id'], '');
	}

	crear_iniciativa(cuit_values) {
		let values = this.form.get_values();
		this.crear_entidad('Lead', values['tax_id'] || '', values['customer_name'] || '');
	}

	crear_cotizacion_iniciativa(cuit_values) {
		let values = this.form.get_values();
		this.crear_cotizacion('Lead', cuit_values['lead']['base_name']);
	}

	crear_cotizacion_cliente(cuit_values) {
		let values = this.form.get_values();
		this.crear_cotizacion('Customer', cuit_values['customer']['base_name']);
	}

	autoasignar(cuit_values) {
		let me = this;
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
					frappe.msgprint(r.message);
					me.fetch_and_render();
				}
			}
		});
	}

	se_puede_mostrar(cuit_values) {
		// Si existe inciativa y no esta asignada o asignada a el usuario logeado
		if (!cuit_values['lead']) {
			return true
		}

		if (!cuit_values['lead']['assign']) {
			return true
		}

		return cuit_values['lead']['assign'].includes(frappe.session.user)
	}

	render(cuit_values) {
		let me = this;
		let customer_html = '';
		let lead_html = '';
		let quotation_html = '';
		let lead_events_html = '';
		let relations_html = '';
		let estado_cuenta = `
		 	<div class="row">
                <div class="col-lg-4 d-flex align-items-stretch">
                    <div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                        <h5 class="border-bottom pb-2">Estado de Cuenta</h5>
                        <h4 class="text-center ${cuit_values['estado_cuit_class']}" style="margin-bottom: 0px;">${cuit_values['estado_cuit']}</h4>
                    </div>
                </div>
                <div class="col-lg-4 d-flex align-items-stretch">
                    <div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                        <h5 class="border-bottom pb-2">Última verificación de NOSIS (días)</h5>
                        <h4 class="text-center text-muted" style="margin-bottom: 0px;">${cuit_values['last_nosis']}</h4>
                    </div>
                </div>
                <div class="col-lg-2 d-flex align-items-stretch">
                    <div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                        <img src="${cuit_values['image']}" class="img-fluid">
                    </div>
                </div>
            </div>
		`

		let contact_table = {};
		let lead_table = {};
		let quotation_table = {};
		let event_table = {};

		if (cuit_values['customer']) {
			let cv = cuit_values['customer']
			contact_table = {
			  	columns: ['Razon Social', 'Cliente', 'Unidad de Negocio', 'Tipo de Servicio', 'Nombre Contacto', 'Domicilio', 'Celular Contacto', 'Mail Contacto', 'Área', 'Puesto', 'Proceso'],
			  	search: true,
			  	data: [
			    	[cv['customer_name'], gridjs.html(cv['name']), '-', '-', cv['contact']['contact_person'], '-', cv['contact']['contact_mobile'], cv['contact']['contact_email'], cv['contact']['area'], cv['contact']['puesto'], cv['contact']['proceso']],
			  	],
			  	language: {
			    	'search': {
			      		'placeholder': 'Buscar...'
			    	},
			    	'pagination': {
				    	'previous': 'Anterior',
				      	'next': 'Siguiente',
				      	'showing': 'Mostrando',
				      	'results': () => 'Registros'
			    	}
			  	}
			};
			customer_html = `
			<div id="caca"></div>
				<div class="row">
                	<div class="col-lg-12 d-flex align-items-stretch">
                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                    		<h5 class="border-bottom pb-2">Contacto</h5>
							<div>
								<div id="contact_table"></div>
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

		if (false) { // TODO relations
			relations_html = `
				<div class="row">
                	<div class="col-lg-12 d-flex align-items-stretch">
                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                    		<h5 class="border-bottom pb-2">Relaciones</h5>
							<div>
								<table class="table table-bordered">
									<tr>
										<th></th>
										<th></th>
										<th></th>
										<th></th>
									</tr>
									<tr>
										<td></td>
										<td></td>
										<td></td>
										<td></td>
									</tr>
								</table>
							</div>
						</div>
					</div>
				</div>
			`;
		} 

		if (cuit_values['lead'] && me.se_puede_mostrar(cuit_values)) {
			let lead_data = cuit_values['lead'];
			lead_table = {
			  	columns: ['Razon Social', 'Fecha', 'Iniciativa', 'Nombre Contacto', 'Celular Contacto', 'Mail Contacto', 'Asignado'],
			  	search: true,
			  	data: [
			    	[lead_data['lead_name'], frappe.datetime.get_datetime_as_string_es(lead_data['creation']), gridjs.html(lead_data['name']), lead_data['contact']['contact_person'], lead_data['contact']['contact_mobile'], lead_data['contact']['contact_email'], gridjs.html(lead_data['assign'])],
			  	],
			  	language: {
			    	'search': {
			      		'placeholder': 'Buscar...'
			    	},
			    	'pagination': {
				    	'previous': 'Anterior',
				      	'next': 'Siguiente',
				      	'showing': 'Mostrando',
				      	'results': () => 'Registros'
			    	}
			  	}
			};

			lead_html = `
				<div class="row">
                	<div class="col-lg-12 d-flex align-items-stretch">
                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                    		<h5 class="border-bottom pb-2">Iniciativa</h5>
							<div>
								<div id="lead_table"></div>
							</div>
						</div>
					</div>
				</div>
			`;

			if (cuit_values['lead']['events'] && me.se_puede_mostrar(cuit_values)) {
				let event_data = []
				for (let i = 0; i < cuit_values['lead']['events'].length; i++) {
					event_data.push([
						gridjs.html(cuit_values['lead']['events'][i]['link']),
						frappe.datetime.get_datetime_as_string_es(cuit_values['lead']['events'][i]['communication_date']),
						cuit_values['lead']['events'][i]['sender_full_name'],
						cuit_values['lead']['events'][i]['event_category'],
						cuit_values['lead']['events'][i]['subject'],
						gridjs.html(cuit_values['lead']['events'][i]['content'])
					])
				}
				event_table = {
				  	columns: ['Evento', 'Fecha', 'Usuario', 'Categoría', 'Asunto', 'Contenido'],
				  	search: true,
				  	data: event_data,
					pagination: {
					    limit: 10,
					    summary: false
					},
				  	language: {
				    	'search': {
				      		'placeholder': 'Buscar...'
				    	},
				    	'pagination': {
					    	'previous': 'Anterior',
					      	'next': 'Siguiente',
					      	'showing': 'Mostrando',
					      	'results': () => 'Registros'
				    	}
				  	}
				};

				lead_events_html = `
					<div class="row">
	                	<div class="col-lg-12 d-flex align-items-stretch">
	                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
	                    		<h5 class="border-bottom pb-2">Histórico</h5>
								<div>
									<div id="event_table"></div>
								</div>
							</div>
						</div>
					</div>
				`;
			} else {

				if (me.se_puede_mostrar(cuit_values)) {
					lead_events_html = `
						<div class="row">
		                	<div class="col-lg-12 d-flex align-items-stretch">
		                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
		                    		<h5 class="border-bottom pb-2">Histórico</h5>
									<h5 class="text-muted">No hay Histórico en esta Iniciativa</h5>
								</div>
							</div>
						</div>
					`
				} else {
					lead_events_html = '';
					
				}
			}
		} else {

			if (me.se_puede_mostrar(cuit_values)) {
				lead_html = `
					<div class="row">
	                	<div class="col-lg-12 d-flex align-items-stretch">
	                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
	                    		<h5 class="border-bottom pb-2">Histórico</h5>
								<h5 class="text-muted">No hay Histórico en esta Iniciativa</h5>
							</div>
						</div>
					</div>
				`

				lead_events_html = `
					<div class="row">
	                	<div class="col-lg-12 d-flex align-items-stretch">
	                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
	                    		<h5 class="border-bottom pb-2">Iniciativa</h5>
								<h5 class="text-muted">No hay Iniciativa con ese CUIT</h5>
							</div>
						</div>
					</div>
				`
			} else {
				lead_html = ''
				lead_events_html = ''
			}
		}

		if (cuit_values['quotations'] && me.se_puede_mostrar(cuit_values)) {
			let quotation_data = []
			for (let i = 0; i < cuit_values['quotations'].length; i++) {
				quotation_data.push([
					gridjs.html(cuit_values['quotations'][i]['name']),
					cuit_values['quotations'][i]['transaction_date'],
					cuit_values['quotations'][i]['contact']['contact_person'],
					cuit_values['quotations'][i]['contact']['contact_mobile'],
					cuit_values['quotations'][i]['contact']['contact_email'],
					gridjs.html(cuit_values['quotations'][i]['assign']),
					gridjs.html('<b>-</b>'),
					gridjs.html('<b>-</b>')
				])
			}
			quotation_table = {
			  	columns: ['Nombre', 'Fecha', 'Nombre Contacto', 'Celular Contacto', 'Mail Contacto', 'Asignado', 'Domicilio de Explotación', 'Unidad de Negocio'],
			  	search: true,
			  	data: quotation_data,
				pagination: {
				    limit: 10,
				    summary: false
				},
			  	language: {
			    	'search': {
			      		'placeholder': 'Buscar...'
			    	},
			    	'pagination': {
				    	'previous': 'Anterior',
				      	'next': 'Siguiente',
				      	'showing': 'Mostrando',
				      	'results': () => 'Registros'
			    	}
			  	}
			};

			quotation_html = `
				<div class="row">
                	<div class="col-lg-12 d-flex align-items-stretch">
                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
                    		<h5 class="border-bottom pb-2">Cotizaciones</h5>
							<div>
								<div id="quotation_table"></div>
							</div>
						</div>
					</div>
				</div>
			`;
		} else {
			if (me.se_puede_mostrar(cuit_values)) {
				quotation_html = `
					<div class="row">
	                	<div class="col-lg-12 d-flex align-items-stretch">
	                    	<div class="card border-0 shadow-sm p-3 mb-3 w-100 rounded-sm" style="background-color: var(--card-bg)">
	                    		<h5 class="border-bottom pb-2">Cotizaciones</h5>
								<h5 class="text-muted">No hay Cotizaciones con ese CUIT</h5>
							</div>
						</div>
					</div>
				`
			} else {
				quotation_html = '';
			}
		}

		let html = `
			${estado_cuenta}
			${customer_html}
			${relations_html}
			${quotation_html}
			${lead_html}
			${lead_events_html}
		`;

		this.form.get_field('preview').html(html);

		if (!$.isEmptyObject(contact_table)) {
			new gridjs.Grid(contact_table).render(document.getElementById("contact_table"));
		}

		if (!$.isEmptyObject(lead_table)) {
			new gridjs.Grid(lead_table).render(document.getElementById("lead_table"));
		}

		if (!$.isEmptyObject(event_table)) {
			new gridjs.Grid(event_table).render(document.getElementById("event_table"));
		}

		if (!$.isEmptyObject(quotation_table)) {
			new gridjs.Grid(quotation_table).render(document.getElementById("quotation_table"));
		}
		
	}
};