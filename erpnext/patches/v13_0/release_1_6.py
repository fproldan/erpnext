from __future__ import unicode_literals

import frappe


def execute():
    frappe.get_doc(
        {
            "name": "¡Nueva actualización 1.6!",
            "title": "¡Nueva actualización 1.6 🚀!",
            "public": 1,
            "notify_on_login": 1,
            "notify_on_every_login": 0,
            "expire_notification_on": "2023-01-05",
            "content": "<div class=\"ql-editor read-mode\"><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/Blog/lanzamiento1.6-1.png\"></p><p><br></p><p>Desde el equipo de DiamoERP estamos felices de anunciar la release V 1.6 de DiamoERP. Hemos trabajado arduamente para seguir ofreciendo un servicio de excelencia, y a continuación les contamos las principales características de la versión actualizada: Nueva integración con TiendaNube, Usuarios reducidos y más.</p><p><br></p><p>¡Esperamos que les gusten tanto como a nosotros!</p><p><br></p><p><strong>Nuevo integración con Tienda Nube</strong></p><p>La nueva integración de Tiendanube permite sincronizar tus ventas, stock y precios en ambos sentidos, y muchas otras configuraciones que hacen a la política de universalizar nuestras integraciones de ecommerces!</p><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/Blog/lanzamiento1.6-2.png\"></p><p><br></p><p><strong>Usuarios Reducidos</strong></p><p>Presentamos esta nueva modalidad para adquirir usuarios específicos, a menor costo: Usuarios Reducidos. Estos usuarios permiten tener grandes plantillas de empleado, pagando menores valores ya que solo acceden a ciertas secciones del sistema. El lanzamiento incluye <strong>Usuario de Ventas</strong>, <strong>Usuario de Proyecto</strong> y <strong>Usuario de HelpDesk</strong>.</p><p><img align=\"center\" src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/Blog/lanzamiento1.6-3.png\" style=\"display: block; margin: auto;\" width=\"610\"></p><p><br></p><p><br></p><p><strong>Usuario Contador</strong></p><p>A partir de esta actualización, hay un tipo de usuario Contador <strong>gratuitamente</strong> incluido para todas las instancias. Esto permite darle acceso para que el contador saque y revise los reportes que necesita, sin consumir un usuario de sistema.</p><p><br></p><p><strong>Nuevo Reporte Estado de pago de ordenes de venta</strong></p><p>Este nuevo reporte permite ver el estado de Ordenes de venta respecto a como están siendo facturadas, para tener un mayor control sobre los pedidos confirmados, pendientes de facturar.</p><p><br></p><p>Agregados menores como Posición fiscal y concepto incluido predeterminado, paginación directa en tablas hijas, podes conectar las entidades clientes y proveedores, mejoras en pago multimoneda, optimizaciones de performance y más en esta actualización, buscando la excelencia de DiamoERP.</p></div>",
            "doctype": "Note",
        }
    ).insert(ignore_mandatory=True)
    frappe.db.commit()
