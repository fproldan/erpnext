from __future__ import unicode_literals

import frappe


def execute():
    frappe.get_doc(
        {
            "name": "¡Nueva actualización 1.3!",
            "title": "¡Nueva actualización 1.3 🚀 !",
            "public": 1,
            "notify_on_login": 1,
            "notify_on_every_login": 0,
            "expire_notification_on": "2022-03-31",
            "content": "<div class=\"ql-editor read-mode\"><p><span style=\"color: rgb(76, 90, 103); background-color: rgb(255, 255, 255);\"><img alt=\"link\" src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.3/actualizacion1.3.jpg\"></span></p><p><br></p><p>Desde el equipo de DiamoERP estamos felices de anunciar la release V 1.3 de DiamoERP. Hemos trabajado arduamente para seguir ofreciendo un servicio de excelencia, y a continuación les contamos las principales características de la versión actualizada: nueva integracion de MercadoLibre.</p><p>¡Esperamos que les gusten tanto como a nosotros!</p><p><br></p><h2>Integración con MercadoLibre 1.0</h2><p>Esta primera interación con la integración de MercadoLibre supuso un enorme desafío, que era dejar las bases para la mejor integración de MercadoLibre para un ERP.</p><p><br></p><p><span style=\"color: rgb(76, 90, 103); background-color: rgb(255, 255, 255);\"><img alt=\"link\" src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/Web/Integraciones/MercadoLibre/logo-mercadolibre.png\"></span></p><p><br></p><p><br></p><p>La integración cumple con sincronizar las ventas, precios y stock, pero destacamos algunas particularidades:</p><p><strong>Sincronización de Precios:</strong> Ahora podes elegir si apliacarle un impuesto arriba al precio de tu lista, evitando de esta forma tener que conformar diferentes listas de precios para ML y los otros canales.</p><p><strong>Sincronización de stock:</strong> Podrás elegir que almacenes son los que van a sincronizar contra ML, dedicar uno a envíos Full, y pausar las publicaciones automáticamente antes de que se queden sin stock.</p><p><strong>Más información para gestionar rápidamente tus pedidos:</strong> Ahora tenes más información en las Ordenes de venta, para poder clasificarlas, crear alertas o reportes, y gestionar rápidamente sus envíos.</p><p><br></p><p><span style=\"color: rgb(76, 90, 103); background-color: rgb(255, 255, 255);\"><img align=\"center\" alt=\"link\" src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/Web/Integraciones/MercadoLibre/mercadolibre1.jpg\" style=\"display: block; margin: auto;\"></span></p><p><span style=\"color: rgb(76, 90, 103); background-color: rgb(255, 255, 255);\">﻿</span></p><h2>Y mucho más </h2><p>Más de 30 correcciones, optimizaciones de performance y más en esta actualización, buscando la excelencia de DiamoERP.</p></div>"
            "doctype": "Note",
        }
    ).insert(ignore_mandatory=True)
    frappe.db.commit()
