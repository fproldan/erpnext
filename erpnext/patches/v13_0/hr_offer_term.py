from __future__ import unicode_literals

from frappe.desk.page.setup_wizard.setup_wizard import make_records
import frappe
from frappe import _


def execute():
	frappe.db.delete("Offer Term")
	frappe.db.commit()
	records = [{"doctype": "Offer Term", "offer_term": _("Incentivos")},
		{"doctype": "Offer Term", "offer_term": _("Período de Preaviso")},
		{"doctype": "Offer Term", "offer_term": _("Francos por Año")},
		{"doctype": "Offer Term", "offer_term": _("Responsabilidades")},
		{"doctype": "Offer Term", "offer_term": _("Descripción del Trabajo")},
		{"doctype": "Offer Term", "offer_term": _("Departamento")},
		{"doctype": "Offer Term", "offer_term": _("Acciones de la empresa")},
		{"doctype": "Offer Term", "offer_term": _("Horas de Trabajo")},
		{"doctype": "Offer Term", "offer_term": _("Beneficios del Empleado")},
		{"doctype": "Offer Term", "offer_term": _("Período de Prueba")},
		{"doctype": "Offer Term", "offer_term": _("Salario Anual")},
		{"doctype": "Offer Term", "offer_term": _("Fecha de incorporación")},]
	make_records(records)
	frappe.db.commit()