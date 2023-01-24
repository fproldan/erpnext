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
def get_cuit(tax_id):
	import json
	from frappe.utils.csvutils import getlink

	customer = (frappe.db.get_all('Customer', {'tax_id': tax_id}) or [{}])[0]
	
	if not customer:
		customer = None
	else:
		customer = frappe.get_doc('Customer', customer['name'])

	leads = (frappe.get_all('Lead', {'tax_id': tax_id}) or [{}])[0]
	if not leads:
		lead = None
	else:
		lead = frappe.get_doc('Lead', leads['name'])

	resp = {
		'customer': '',
		'lead': '',
		'estado_cuit': '',
		'estado_cuit_class': ''
	}

	if not customer and not lead:
		return resp

	if lead:
		resp['lead'] = {
			'name': getlink('Lead', lead.name),
			'base_name': lead.name,
			'lead_name': lead.lead_name,
			'assign': ",".join(getlink('User', a) for a in json.loads(lead._assign or '[]'))
		}

	if customer:
		resp['customer'] = {
			'name': getlink('Customer', customer.name),
			'customer_name': customer.customer_name,
		}
		
	if lead:
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
def autoasignar(name, user):
	from frappe.desk.form.assign_to import add as add_assignemnt
	add_assignemnt({
		'doctype': 'Lead',
		'name': name,
		'assign_to': user
	})
	frappe.db.commit()
