import frappe


def execute():
	for u in frappe.get_all('User'):
		user = frappe.get_doc('User', u)
		user_roles = [r.role for r in user.roles]

		if 'Auditor' in user_roles:
			user.remove_roles("Auditor")

		frappe.db.commit()