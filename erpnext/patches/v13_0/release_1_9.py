from __future__ import unicode_literals

import frappe


def execute():
    if not frappe.db.exists('Note', {'name': "¡Nueva actualización 1.9!"}):
        frappe.get_doc(
            {
                "name": "¡Nueva actualización 1.9!",
                "title": "¡Nueva actualización 1.9 🚀!",
                "public": 1,
                "notify_on_login": 1,
                "notify_on_every_login": 0,
                "expire_notification_on": "",
                "content": "<div class=\"ql-editor read-mode\"><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.9/1.9.jpg\"></p><p><br></p><p>Desde el equipo de DiamoERP estamos felices de anunciar la release V 1.9 de DiamoERP. Hemos trabajado arduamente para seguir ofreciendo un servicio de excelencia, y a continuación les contamos las principales características de la versión actualizada: **Grandes mejoras en la integración de Woocommerce y otras novedades**.</p><p><br></p><p>¡Esperamos que les gusten tanto como a nosotros!</p><p><br></p><p>## Woocommerce Envíos</p><p><br></p><p>Ahora los envíos no se sincronizan más como producto, sino que utilizan la Regla de envío para esto. Permitiendo que se pueda utilizar de forma universal el tema de envíos, mejorando la forma en que podemos filtrarlo y analizarlos en una posterior instancia. También facilita que se pueda visualizar de forma más clara en las impresiones.</p><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.9/2.png\"></p><p><br></p><p>## Woocommerce Términos de Pagos</p><p><br></p><p>Ahora es posible sincronizar los descuentos de pago que se configuren en Woocommerce, con los Términos de pago del sistema. De esta forma se podrán efectuar correctamente los descuentos en las OV, con el mismo concepto que envíos, utilizándolo de forma transparente al usuario con los mismos términos de pago que utiliza en otros canales.</p><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.9/1.png\"></p><p><br></p><p>## Cálculo de Precio para bundles</p><p><br></p><p>Sumamos una alternativa a las herramientas de cálculo para precios de bundles existente, donde cada bundle tiene la opción ahora de poder calcular el precio sumando los productos que lo consumen, y de esta forma, este nuevo precio que se genera, se puede enviar a los ecommerces/Mercadolibre sin problema en las actualizaciones masivas.</p><p><br></p><p>## Balance Multimoneda</p><p><br></p><p>Ahora tenemos la opción de ver el balance en otra moneda, tomando como referencia el tipo de cambio del comprobante.</p><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.9/3.png\"></p><p><br></p><p>## Y mucho más..</p><p><br></p><p>Agregados menores como seleccionar múltiples Almacenes en el reporte Inventario Proyectado, envío por mail del Libro de IVA en tamaños grandes, correcciones en sincronizaciones de ecommerces, optimizaciones de performance y más en esta actualización, buscando la excelencia de DiamoERP.</p></div>",
                "doctype": "Note",
            }
        ).insert(ignore_mandatory=True)
        frappe.db.commit()


