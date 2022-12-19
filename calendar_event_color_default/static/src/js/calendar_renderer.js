odoo.define('calendar_event_color_default.calendar_rederer', function (require) {
    "use strict";

    var CalendarRenderer = require('web.CalendarRenderer');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;

    CalendarRenderer.include({
        _eventRender: function (event) {
            var res = this._super.apply(this, arguments);
            var color = this.getColor(event.extendedProps.color_index);

            //Se asigna el indice de color por cada condición
            if (event.extendedProps && event.extendedProps.record && event.extendedProps.record["x_studio_servicios_1"]){
                if (event.extendedProps.record["x_studio_servicios_1"] && event.extendedProps.record.x_studio_servicios_1 == "Paciente de primera vez - Estudio de la marcha y postura + Plantillas ortopédicas") {
                    color = 2;
                } else if (event.extendedProps.record["x_studio_servicios_1"] && event.extendedProps.record.x_studio_servicios_1 == "Paciente de seguimiento - Estudio de la marcha y postura + Renovación de plantillas ortopédicas") {
                    color = 4;
                } else if (event.extendedProps.record["x_studio_servicios_1"] && event.extendedProps.record.x_studio_servicios_1 == "Cita para revisión de plantillas ortopédicas (Ya en uso)") {
                    color = 10;
                } else if (event.extendedProps.record["x_studio_servicios_1"] && event.extendedProps.record.x_studio_servicios_1 == "Consulta en línea") {
                    color = 9;
                } else if (event.extendedProps.record["x_studio_servicios_1"] && event.extendedProps.record.x_studio_servicios_1 == "Primera visita fisioterapia") {
                    color = 23;
                } else if (event.extendedProps.record["x_studio_servicios_1"] && event.extendedProps.record.x_studio_servicios_1 == "Elaboración de plantillas ortopédicas personalizadas, con receta médica (Sin estudio)") {
                    color = 21;
                }
            }

            var qweb_context = {
                event: event,
                record: event.extendedProps.record,
                color: color,
                showTime: !self.hideTime && event.extendedProps.showTime,
            };
            this.qweb_context = qweb_context;
            if (_.isEmpty(qweb_context.record)) {
                return '';
            } else {
                return qweb.render("calendar-box", qweb_context);
            }
            return res;
        }
    });
});