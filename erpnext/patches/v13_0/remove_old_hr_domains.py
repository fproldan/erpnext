import frappe
import erpnext.hooks as hooks

def execute():
	if not frappe.db.exists("Domain", "HR Asistencia, Vacaciones y Rendimiento de Gastos"):
		d = frappe.new_doc('Domain')
		d.name = 'HR Asistencia, Vacaciones y Rendimiento de Gastos'
		d.domain = 'HR Asistencia, Vacaciones y Rendimiento de Gastos'
		d.save()
		frappe.db.commit()

	hooks.after_migrate.append("erpnext.patches.v13_0.remove_old_hr_domains.remove_old_hr_domains")


def remove_old_hr_domains():
	frappe.flags.in_patch = True
	frappe.db.delete('Has Domain', {'domain': 'HR Asistencia y Vacaciones'})
	frappe.db.delete('Has Domain', {'domain': 'HR Reclutamiento, Capacitacion y Gastos'})
	frappe.delete_doc('Domain', 'HR Asistencia y Vacaciones', ignore_missing=True)
	frappe.delete_doc('Domain', 'HR Reclutamiento, Capacitacion y Gastos', ignore_missing=True)

	ds = frappe.get_doc('Domain Settings')
	for ad in ds.active_domains:
		if ad.domain in ['HR Asistencia y Vacaciones', 'HR Reclutamiento, Capacitacion y Gastos']:
			ad.delete()

	ds.save()
	frappe.db.commit()