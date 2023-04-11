import frappe


def update_lead_phone_numbers(contact, method):
	if contact.phone_nos:
		contact_lead = contact.get_link_for("Lead")
		if contact_lead:
			phone = mobile_no = contact.phone_nos[0].phone

			if len(contact.phone_nos) > 1:
				# get the default phone number
				primary_phones = [phone_doc.phone for phone_doc in contact.phone_nos if phone_doc.is_primary_phone]
				if primary_phones:
					phone = primary_phones[0]

				# get the default mobile number
				primary_mobile_nos = [phone_doc.phone for phone_doc in contact.phone_nos if phone_doc.is_primary_mobile_no]
				if primary_mobile_nos:
					mobile_no = primary_mobile_nos[0]

			lead = frappe.get_doc("Lead", contact_lead)
			lead.db_set("phone", phone)
			lead.db_set("mobile_no", mobile_no)



@frappe.whitelist()
def get_cuit(tax_id=None, customer_name=None):
	import json
	from frappe.utils.csvutils import getlink
	from frappe.contacts.doctype.contact.contact import get_contact_details
	from frappe.desk.form.load import get_communication_data
	from erpnext.accounts.party import get_default_contact

	if tax_id:
		tax_id = tax_id.strip()
		customer = (frappe.db.get_all('Customer', {'tax_id': tax_id}) or [{}])[0]

	if customer_name:
		customer = (frappe.db.get_all('Customer', {'name': customer_name}) or [{}])[0]

	customer_contact_details = {
		'contact_person': '',
		'contact_display': '',
		'contact_email': '',
		'contact_mobile': '',
		'contact_phone': '',
	}

	lead_contact_details = {
		'contact_person': '',
		'contact_display': '',
		'contact_email': '',
		'contact_mobile': '',
		'contact_phone': '',
	}

	if not customer:
		customer = None
	else:
		customer = frappe.get_doc('Customer', customer['name'])
		customer_contact = get_default_contact(customer.doctype, customer.name, '')
		if customer_contact:
			customer_contact_details = get_contact_details(customer_contact)

	leads = (frappe.get_all('Lead', {'tax_id': tax_id}) or [{}])[0]
	if not leads:
		lead = None
	else:
		lead = frappe.get_doc('Lead', leads['name'])
		lead_contact = get_default_contact(lead.doctype, lead.name, '')
		if lead_contact:
			lead_contact_details = get_contact_details(lead_contact)

	nosis = (frappe.get_all('Verificacion NOSIS', {'cuit': tax_id}, order_by='-fecha') or [{}])[0]
	if not nosis:
		nosis = None
		last_nosis = '-'
	else:
		nosis = frappe.get_doc('Verificacion NOSIS', nosis['name'])
		last_nosis = nosis.get_dias()

	resp = {
		'customer': '',
		'lead': '',
		'estado_cuit': '-',
		'estado_cuit_class': '',
		'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWCAYAAAA8AXHiAAABDklEQVR42u3SMQEAAAQAMJJL4VJWAadzy7Cc6Qp4lmIhFmIhlliIhViIBWIhFmKBWIiFWCAWYiEWiIVYiAViIRZigViIhVggFmIhFoiFWIgFYiEWYoFYiIVYIBZiIRaIhViIBWIhFmKBWIiFWCAWYiEWiIVYiAViIRZigViIhVggFmIhFoiFWIgFYiEWYoFYiIVYIBZiIRaIhViIBWIhFmKBWIiFWCAWYiEWYomFWIiFWCAWYiEWiIVYiAViIRZigViIhVggFmIhFoiFWIgFYiEWYoFYiIVYIBZiIRaIhViIBWIhFmKBWIiFWCAWYiEWiIVYiAViIRZigViIhVggFmIhFoiFWIgFYiEWYsFtAbdmWALgJXnzAAAAAElFTkSuQmCC',
		'last_nosis': last_nosis
	}

	if not customer and not lead:
		return resp


	quotation_search = []
	q_assign = []
	l_assign = []

	if lead:
		events = []
		for communication in get_communication_data(lead.doctype, lead.name, limit=100):
			if communication['reference_doctype'] == 'Event':
				communication['event_category'] = _(communication['communication_medium'])
				communication['link'] = getlink('Event', communication['reference_name'])
				events.append(communication)

		quotation_search.append(lead.name)
		resp['lead'] = {
			'name': getlink('Lead', lead.name),
			'base_name': lead.name,
			'lead_name': lead.lead_name,
			'assign': ",".join(getlink('User', a) for a in json.loads(lead._assign or '[]')),
			'creation': lead.creation,
			'contact': lead_contact_details,
			'events': events,
		}
		l_assign += json.loads(lead._assign or '[]')

	if customer:
		quotation_search.append(customer.name)
		resp['customer'] = {
			'name': getlink('Customer', customer.name),
			'base_name': customer.name,
			'customer_name': customer.customer_name,
			'contact': customer_contact_details,
		}
		if customer.image:
			resp['image'] = customer.image
		
	
	quotations = [frappe.get_doc('Quotation', quotation['name']) for quotation in frappe.get_all('Quotation', {'party_name': ('in', quotation_search)})]
	
	if quotations:
		quotation_contact_details = {
			'contact_person': '',
			'contact_display': '',
			'contact_email': '',
			'contact_mobile': '',
			'contact_phone': '',
		}

		resp['quotations'] = []

		for quotation in quotations:
			quotation_contact = get_default_contact(quotation.doctype, quotation.name, '')
			if quotation_contact:
				quotation_contact_details = get_contact_details(quotation_contact)

			if quotation.status == 'Open':
				status_color = 'text-success'
			else:
				status_color = ''
			link = getlink('Quotation', quotation.name)

			resp['quotations'].append({
				'name': link[:2] + ' class="'+ status_color+'"' + link[2:],
				'base_name': quotation.name,
				'transaction_date': quotation.transaction_date,
				'quotation_to': quotation.quotation_to,
				'party_name': quotation.party_name,
				'assign':  ",".join(getlink('User', a) for a in json.loads(quotation._assign or '[]')),
				'contact': quotation_contact_details,
				'status_color': status_color,
			})

		for q in quotations:
			q_assign += json.loads(q._assign or '[]')

	if q_assign or l_assign:
		resp['estado_cuit'] = 'Activo'
		resp['estado_cuit_class'] = 'text-success'
	else:
		resp['estado_cuit'] = 'Inactivo'
		resp['estado_cuit_class'] = 'text-secondary'

	if customer and customer.disabled:
		resp['estado_cuit'] = 'Inhabilitado'
		resp['estado_cuit_class'] = 'text-danger'

	return resp


@frappe.whitelist()
def crear_entidad(doctype, tax_id):
	target = frappe.new_doc(doctype)
	target.tax_id = tax_id
	return target


@frappe.whitelist()
def crear_cotizacion(quotation_to, party_name):
	target = frappe.new_doc('Quotation')

	target.quotation_to = quotation_to
	target.party_name = party_name
	return target


@frappe.whitelist()
def autoasignar(name, user):
	from frappe.desk.form.assign_to import add as add_assignemnt

	add_assignemnt({
		'doctype': 'Lead',
		'name': name,
		'assign_to': [user]
	})
	frappe.db.commit()
	return f"Usuario {user} asignado a la Iniciativa {name}"
