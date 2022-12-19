odoo.define('gtm_appointments.appointment_form', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var websiteCalendarForm = publicWidget.registry.websiteCalendarForm;


websiteCalendarForm.include({
    events: _.extend({}, websiteCalendarForm.prototype.events, {
        'submit .appointment_submit_form': '_on_submit_appointment'
    }),

    _on_submit_appointment: function (ev) {
        if (window.dataLayer) {
            var days_of_week = [
                'domingo', 'lunes', 'martes', 'miércoles', 'jueves',
                'viernes', 'sábado'
            ];

            var appointment_datetime = $(ev.target).find('input[name="datetime_str"]').first().val();
            var [date, time] = appointment_datetime.split(' ');
            var branch = ev.target.action.match(/(calendar\/)(.*?)(-[0-9]+\/submit)/)[2];
            var date_object = new Date(appointment_datetime);
            var day_of_week = days_of_week[date_object.getDay()];

            window.dataLayer.push({
                'event': 'cita_registrada',
                'dia_cita': date,
                'hora_cita': time,
                'dia_semana': day_of_week,
                'sucursal': branch
            });
        }
    }
});

});
