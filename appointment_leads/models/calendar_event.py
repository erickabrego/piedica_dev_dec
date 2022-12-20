# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    x_sale_order_state = fields.Selection(string="Estado de orden de venta", selection=[("draft","Cotización"),("sent","Cotización enviada"),("sale","Orden de venta"),("done","Bloqueado"),("cancel","Cancelado")], compute="_get_sale_order_state",store=True)
    partner_ids = fields.Many2many(
        'res.partner', 'calendar_event_res_partner_rel',
        string='Attendees', default=False)
    x_personal_schedule_appointment = fields.Selection(string="¿Agendo cita presencial?", selection=[("Sí","Sí"),("No","No")])

    #Relaciona la oportunidad del contacto con la reuinión que se está creando
    @api.model
    def create(self, vals):
        res = super(CalendarEvent, self).create(vals)
        try:
            res.get_opportunity_partner()
        except Exception as e:
            _logger.info(e)
        return res

    def write(self, values):
        res = super(CalendarEvent, self).write(values)
        for rec in self:
            if values.get("x_studio_paciente_confirm_asistencia") and rec.x_studio_paciente_confirm_asistencia and rec.opportunity_id:
                crm_stage = self.env["crm.stage"].sudo().search([("name","=","Agenda cita")],limit=1)
                if crm_stage:
                    rec.opportunity_id.stage_id = crm_stage.id
            if values.get("x_studio_paciente_asisti_a_cita") and rec.x_studio_paciente_asisti_a_cita and rec.opportunity_id and not rec.x_studio_paciente_cancel_cita:
                crm_stage = self.env["crm.stage"].sudo().search([("name","=","Asiste a cita")],limit=1)
                if crm_stage:
                    rec.opportunity_id.stage_id = crm_stage.id
            elif values.get("x_studio_paciente_asisti_a_cita") and rec.x_studio_paciente_asisti_a_cita and rec.opportunity_id and rec.x_studio_paciente_cancel_cita:
                raise ValidationError("La cita ya se encuentra cancelada por el paciente, no es posible marcar como asistió.")
            if values.get("x_studio_paciente_cancel_cita") and rec.x_studio_paciente_cancel_cita and rec.opportunity_id and not rec.x_studio_paciente_asisti_a_cita:
                crm_stage = self.env["crm.stage"].sudo().search([("name","=","Cancela cita")],limit=1)
                if crm_stage:
                    rec.opportunity_id.stage_id = crm_stage.id
            elif values.get("x_studio_paciente_cancel_cita") and rec.x_studio_paciente_cancel_cita and rec.opportunity_id and  rec.x_studio_paciente_asisti_a_cita:
                raise ValidationError("El paciente ya asistio a su cita, no es posible marcar como cancelada.")            
            
            if values.get("partner_ids"):
                try:
                    rec.get_opportunity_partner()
                except Exception as e:
                    _logger.info(e)
        return res

    @api.depends("opportunity_id","opportunity_id.order_ids","opportunity_id.order_ids.state")
    def _get_sale_order_state(self):
        for rec in self:
            if rec.opportunity_id and rec.opportunity_id.order_ids.filtered(lambda line: line.state not in ['draft', 'sent', 'cancel']):
                order_id = rec.opportunity_id.order_ids.filtered(lambda line: line.state not in ['draft', 'sent', 'cancel'])[0]
                rec.x_sale_order_state = "sale"
            elif rec.opportunity_id and rec.opportunity_id.order_ids.filtered(lambda line: line.state not in ['done', 'sale']):
                order_id = rec.opportunity_id.order_ids.filtered(lambda line: line.state not in ['done', 'sale'])[0]
                rec.x_sale_order_state = order_id.state
            else:
                rec.x_sale_order_state = False

    def get_opportunity_partner(self):
        for rec in self:
            stage_id = self.env["crm.stage"].sudo().search([("name", "=", "Agenda cita")], limit=1)
            for partner_id in rec.partner_ids:
                if partner_id:
                    opportunity_ids = self.env["crm.lead"].sudo().search([("partner_id.id", "=", partner_id.id), (
                    "stage_id.name", "in", ["Contactado", "Cancela cita"])])
                    archived_opportunity = self.env["crm.lead"].sudo().search(
                        [("partner_id.id", "=", partner_id.id), ("active", "=", False)])
                    if opportunity_ids and stage_id:
                        for opportunity_id in opportunity_ids:
                            opportunity_id.stage_id = stage_id.id
                            rec["opportunity_id"] = opportunity_id.id
                            rec.opportunity_id.x_calendar_event = rec.id
                    if archived_opportunity and stage_id:
                        for archived_oppo in archived_opportunity:
                            archived_oppo.stage_id = stage_id.id
                            archived_oppo.active = True
                            rec["opportunity_id"] = archived_opportunity.id
                            rec.opportunity_id.x_calendar_event = rec.id

    def open_default_lead(self):
        view = self.env.ref('appointment_leads.default_lead_event_view_form')
        partner_id = self.partner_ids.filtered(lambda partner: partner.x_studio_es_paciente)
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ("Alerta de oportunidad"),
                'message': "No hay un paciente dentro de los participantes del evento.",
                'type': 'warning',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
        if not partner_id:
            return notification
        return {
            'name': 'Oportunidad del paciente',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'default.lead.event',
            'target': 'new',
            'views': [[view.id, 'form']],
            'context': dict(self._context,
                            default_partner_id=partner_id[0].id if partner_id else False,
                            default_event_id=self.id,
            ),
        }      