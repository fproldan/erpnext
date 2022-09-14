from __future__ import unicode_literals

import frappe


def execute():
    frappe.get_doc(
        {
            "name": "¡Nueva actualización 1.5!",
            "title": "¡Nueva actualización 1.5 🚀!",
            "public": 1,
            "notify_on_login": 1,
            "notify_on_every_login": 0,
            "expire_notification_on": "2022-10-01",
            "content": "<div class=\"ql-editor read-mode\"><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.5/imagen1.jpg\"></p><p><br></p><p>Desde el equipo de DiamoERP estamos felices de anunciar la release V 1.5 de DiamoERP. Hemos trabajado arduamente para seguir ofreciendo un servicio de excelencia, y a continuación les contamos las principales características de la versión actualizada: Nuevo módulo de RRHH, Mejoras de Cheques y más</p><p><br></p><p>¡Esperamos que les gusten tanto como a nosotros!</p><p><br></p><p><strong>Nuevo módulo de Recursos Humanos</strong></p><p>Incorporamos este nuevo módulo para el manejo de registros completos de empleados, adquisición de talento, entrenamientos y mucho más.</p><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.5/imagen2.png\"></p><p><br></p><p><strong>Nueva integración con Woocomerce</strong></p><p>La nueva integración de Woocomerce permite sincronizar tus ventas, stock y precios en ambos sentidos, y muchas otras configuraciones que hacen a la política de universalizar nuestras integraciones de ecommerces!</p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.5/imagen3.png\" width=\"610\"></p><p><br></p><p><br></p><p><strong>Comisiones por productos para vendedores</strong></p><p>Ahora los vendedores, pueden comisionar por producto, y verlo reflejado en todos los reportes ya incluido</p><p><br></p><p><strong style=\"color: rgb(31, 39, 46);\">Mejoras en Cheques</strong></p><p>Mejoras para el uso más sencillo de Echeq y la incorporación de la Custodia para todos los cheques!</p><p><br></p><p>Correcciones menores en Suscripciones, Entradas de Pago en diferentes monedas, optimizaciones de performance y más en esta actualización, buscando la excelencia de DiamoERP.</p></div>",
            "doctype": "Note",
        }
    ).insert(ignore_mandatory=True)
    frappe.db.commit()
