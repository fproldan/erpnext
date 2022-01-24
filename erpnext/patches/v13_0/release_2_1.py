from __future__ import unicode_literals

import frappe


def execute():
    frappe.get_doc(
        {
            "name": "¡Nueva actualización 1.2!",
            "title": "¡Nueva actualización 1.2 🚀 !",
            "public": 1,
            "notify_on_login": 1,
            "notify_on_every_login": 0,
            "expire_notification_on": "2022-01-31",
            "content": "<div class=\"ql-editor read-mode\"><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/299e31829e31601a0766bb44883c60c3784f4b5a/Blog/lanzamiento1.2.png\"></p><p><br></p><p>¡Desde el equipo de Diamo estamos felices de anunciar la release V 1.2 de DiamoERP!</p><p><br></p><p>¡Esperamos que les guste tanto como a nosotros!</p><p><br></p><h3>Incorporación del módulo Activos - Bienes</h3><p><br></p><ol><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Podrás gestionar tus activos como maquinarias, equipos informáticos, utilitarios, etc.</li><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Gestionar amortizaciones automáticas en base distintas fórmulas.</li><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Llevar info detallada de compra, seguro, etc.</li><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Crear cronogramas de mantenimiento preventivo para estos activos y llevar un detalle del mismo.</li></ol><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.2/activos.png\" width=\"421\"></p><p><br></p><p><br></p><h3>Incorporación del módulo Sitio Web</h3><p><br></p><ol><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Podrás crear páginas web de forma simple, rápido y sin conocimiento técnico.</li><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>¡Tiene varias plantillas predefinidas para que simplemente reemplaces texto e imágenes!</li><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Formularios web para que autocompleten información de tu sistema.</li><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Portal de clientes para que puedan ver sus documentos e interactuar cargando cotizaciones, pedidos y más.</li><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Analiza las visitas, utiliza el blog, o crea una base de conocimiento para tus clientes.</li></ol><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.2/sitio-web.png\" width=\"430\"></p><p><br></p><h3>Incorporación del submódulo RMA</h3><p><br></p><ol><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Gestiona las garantías de tus productos serializados de forma simple y rápido.</li><li data-list=\"bullet\"><span class=\"ql-ui\" contenteditable=\"false\"></span>Intercomunicado con el módulo de soporte.</li></ol><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.2/rma.png\" width=\"335\"></p><p><br></p><h3>Y mucho más</h3><p><br></p><p><strong>Modificación de las campos que ves en tabla</strong>: esto permite elegir de forma fácil e intuitiva en todos los documentos del sistema qué se ve y qué se modifica por cuenta propia.</p><p><br></p><p><img src=\"https://raw.githubusercontent.com/federicocalvo/DiamoERP-images/main/release-notes/1.2/config-columnas.png\" width=\"223\"></p></div>",
            "doctype": "Note",
        }
    ).insert(ignore_mandatory=True)
    frappe.db.commit()
