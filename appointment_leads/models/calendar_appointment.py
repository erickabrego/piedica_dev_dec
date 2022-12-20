from odoo import models, fields


class CalendarAppointmentType(models.Model):
    _inherit = 'calendar.appointment.type'

    p_lead_create = fields.Boolean(string='Crear oportunidades')
