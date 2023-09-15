from __future__ import unicode_literals

import frappe


def execute():
    if not frappe.db.exists('Note', {'name': "¡Nueva actualización 1.8!"}):
        frappe.get_doc(
            {
                "name": "¡Nueva actualización 1.8!",
                "title": "¡Nueva actualización 1.8 🚀!",
                "public": 1,
                "notify_on_login": 1,
                "notify_on_every_login": 0,
                "expire_notification_on": "",
                "content": "<div class=\"ql-editor read-mode\"><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.8/1.8.png\"></p><p><br></p><p>Desde el equipo de DiamoERP estamos felices de anunciar la release V 1.8 de DiamoERP. Hemos trabajado arduamente para seguir ofreciendo un servicio de excelencia, y a continuación les contamos las principales características de la versión actualizada: <strong>Nuevo submódulo de RRHH, Herramienta Reglas de Autorización, y más</strong>.</p><p><br></p><p>¡Esperamos que les gusten tanto como a nosotros!</p><p><br></p><h2>Nuevo submódulo de RRHH - Asistencia, Vacaciones y Rendimiento de Gastos</h2><p><br></p><p>Este nuevo submódulo atiende todas las necesidades para la gestión de los empleados, fácil, completa e integrada con las demás funciones existentes. El <strong>control de asistencias de múltiples fomras</strong> (inclusive automática por login), la <strong>asignación y gestión de Vacaciones y Licencias</strong>, para calcular automáticamente los días que le corresponde a cada uno ayudan a no depender de agencias externas. Y las <strong>herramientas de Rendimientos de Gastos</strong>, podrán solicitar, aprobar o rechazar todos los gastos que los empleados reclamen, de forma ordenada y en pocos clicks.</p><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.8/rembolso-gastos.png\"></p><p><br></p><p><br></p><h2>Nueva herramienta Reglas de Autorización</h2><p><br></p><p>Con esta nueva herramienta, vas a poder crear fácilmente reglas para que muchos documentos necesiten de un mayor nivel de permisos para aprobar la transacción. Por ejemplo, evita que los vendedores Validen ventas mayores $50.000, sin la aprovación de un gerente.</p><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.8/reglas-autorizacion.png\"></p><p><br></p><p><br></p><h2>Vista previa de retenciones</h2><p><br></p><p>Ahora aquellos usuarios avanzados que quieran tener un mejor conocimiento de como se está generando la retención, tanto antes como después de validar la Entrada de Pago, podrán hacerlo a través del botón visualizar retención. Tendrán una explicación clara y sencilla para revisar la misma o controlar los datos ingresados.</p><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.8/retencion.png\"></p><p><br></p><p><br></p><p><br></p><p>Agregados menores como Importación de Servicios, correcciones en Conciliador Bancario, Sincronización de Estados de Woocomerce, optimizaciones de performance y más en esta actualización, buscando la excelencia de DiamoERP.</p></div>",
                "doctype": "Note",
            }
        ).insert(ignore_mandatory=True)
        frappe.db.commit()