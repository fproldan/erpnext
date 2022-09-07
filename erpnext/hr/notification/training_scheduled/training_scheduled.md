<table class="panel-header" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr height="10"></tr>
    <tr>
        <td width="15"></td>
        <td>
            <div class="text-medium text-muted">
                <span>Evento de Capacitación: {{ doc.event_name }}</span>
            </div>
        </td>
        <td width="15"></td>
    </tr>
    <tr height="10"></tr>
</table>

<table class="panel-body" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr height="10"></tr>
    <tr>
        <td width="15"></td>
        <td>
            <div>
                {{ doc.introduction }}
                <ul class="list-unstyled" style="line-height: 1.7">
                    <li>Lugar del evento: <b>{{ doc.location }}</b></li>
                    {% set start = frappe.utils.get_datetime(doc.start_time) %}
                    {% set end = frappe.utils.get_datetime(doc.end_time) %}
                    {% if start.date() == end.date() %}
                        <li>Fecha: <b>{{ start.strftime("%A, %d %b %Y") }}</b></li>
                        <li>
                            Tiempo: <b>{{ start.strftime("%I:%M %p") + ' a ' + end.strftime("%I:%M %p") }}</b>
                        </li>
                    {% else %}
                        <li>
                            Hora de inciio: <b>{{ start.strftime("%A, %d %b %Y at %I:%M %p") }}</b>
                        </li>
                        <li>Hora de fin: <b>{{ end.strftime("%A, %d %b %Y at %I:%M %p") }}</b></li>
                    {% endif %}
                    <li>Enlace al evento: {{ frappe.utils.get_link_to_form(doc.doctype, doc.name) }}</li>
                    {% if doc.is_mandatory %}
                        <li>Nota: Esta capacitación es obligatorio</li>
                    {% endif %}
                </ul>
            </div>
        </td>
        <td width="15"></td>
    </tr>
    <tr height="10"></tr>
</table>