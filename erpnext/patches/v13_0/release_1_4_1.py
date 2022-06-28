from __future__ import unicode_literals

import frappe


def execute():
    frappe.get_doc(
        {
            "name": "¡Nueva actualización 1.4.1!",
            "title": "¡Nueva actualización 1.4.1 🚀!",
            "public": 1,
            "notify_on_login": 1,
            "notify_on_every_login": 0,
            "expire_notification_on": "2022-07-01",
            "content": "<div class=\"ql-editor read-mode\"><p>Desde el equipo de DiamoERP estamos felices de anunciar la release V 1.4.1 de DiamoERP con varias novedades y correcciones.</p><p><br></p><p>¡Esperamos que les gusten tanto como a nosotros!</p><p><br></p><p><strong>Nueva Herramienta de Actualización de Precios Masiva por lista de Compra</strong></p><p>Ahora podrás actualizar los precios de venta, a través de las listas de compras.</p><p><br></p><p><strong style=\"\">Liquidador de comisiones a vendedores</strong></p><p><span style=\"\">Con esta nueva herramienta se podrá liquidar y pagar fácilmente las comisiones a los vendedores</span></p><p><br></p><p><strong>Nuevo Flujo de Efectivo</strong></p><p>Un nuevo Flujo de Efectivo permitirá analizar de forma más sencilla su estado Financiero.</p><p><br></p><p><strong>Nuevos controles para Libro de IVA</strong></p><p>Los comprobantes poseen más controles para evitar errores en la importación de los libros de IVA.</p><p><br></p><p>Y muchas otras correcciones, optimizaciones y pequeños cambios para mejorar la experiencia!</p></div>",
            "doctype": "Note",
        }
    ).insert(ignore_mandatory=True)
    frappe.db.commit()
