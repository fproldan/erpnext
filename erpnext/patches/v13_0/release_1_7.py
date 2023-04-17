from __future__ import unicode_literals

import frappe


def execute():
    frappe.get_doc(
        {
            "name": "¡Nueva actualización 1.7!",
            "title": "¡Nueva actualización 1.7 🚀!",
            "public": 1,
            "notify_on_login": 1,
            "notify_on_every_login": 0,
            "expire_notification_on": "2023-04-30",
            "content": "<div class=\"ql-editor read-mode\"><p><img src=\"/files/DkjUDaa.jpg\"></p><p><br></p><p>Desde el equipo de DiamoERP estamos felices de anunciar la release V 1.7 de DiamoERP. Hemos trabajado arduamente para seguir ofreciendo un servicio de excelencia, y a continuación les contamos las principales características de la versión actualizada: Optimización de consultas y rendimiento, para mayor velocidad de acceso a los datos.</p><p><br></p><p>¡Esperamos que les gusten tanto como a nosotros!</p><p><br></p><h3>Hasta 1.5X más rápido!</h3><p><br></p><p>Sabemos que el tiempo es un recurso valioso para cualquier empresa, y nuestro ERP mejorado puede ayudarte a ahorrar tiempo y aumentar tu productividad. DiamoERP ha mejorado su velocidad en hasta 50% en algunos escenarios, lo que significa que ahora puedes completar tus tareas diarias en la mitad del tiempo.</p><p><br></p><p><img src=\"/files/Xdd8Go5.png\"></p><p><br></p><p>1.4 X en Consultas, 1.2 X en Transacciones y hasta 1.5 X en consultas de reportes!</p><p><br></p><h3>Módulo Web Discusiones</h3><p><br></p><p>Con un simple click, agregar el módulo discusiones a tus páginas web permite que tu público interactúe de una forma sencilla y sin plugins de terceros.</p><p><br></p><p><img align=\"center\" src=\"/files/9CqXZAQ.png\" style=\"display: block; margin: auto;\" width=\"705\"></p><p><br></p><h3><strong>Mejoras en nuestra plataforma de Documentación</strong></h3><p><br></p><p>Nuevos menús de navegación y utilidades para que encontrar lo que estás buscando sea más intuitivo, y toda la información que necesitas este en el lugar correcto.</p><p><br></p><p>Agregados menores como correcciones en Conciliador Bancario, Reportes contables, agregados de nuevos tipos de comprobantes , optimizaciones de performance y más en esta actualización, buscando la excelencia de DiamoERP.</p><p><br></p></div>",
            "doctype": "Note",
        }
    ).insert(ignore_mandatory=True)
    frappe.db.commit()
