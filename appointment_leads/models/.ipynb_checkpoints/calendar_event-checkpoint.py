# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    x_sale_order_state = fields.Selection(string="Estado de orden de venta", selection=[("draft","Cotización"),("sent","Cotización enviada"),("sale","Orden de venta"),("done","Bloqueado"),("cancel","Cancelado")], compute="_get_sale_order_state",store=True)
    partner_ids = fields.Many2many(
        'res.partner', 'calendar_event_res_partner_rel',
        string='Attendees', default=False)

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
            if values.get("x_studio_paciente_asisti_a_cita") and rec.x_studio_paciente_asisti_a_cita and rec.opportunity_id:
                crm_stage = self.env["crm.stage"].sudo().search([("name","=","Asiste a cita")],limit=1)
                if crm_stage:
                    rec.opportunity_id.stage_id = crm_stage.id
            elif values.get("x_studio_paciente_agend_cita_presencial") and rec.x_studio_paciente_agend_cita_presencial == "Sí" and rec.opportunity_id and rec.opportunity_id.stage_id.name == "Agenda cita virtual":
                crm_stage = self.env["crm.stage"].sudo().search([("name","=","Agenda cita")],limit=1)
                rec.opportunity_id.stage_id = crm_stage.id
            elif values.get("x_studio_paciente_agend_cita_presencial") and rec.x_studio_paciente_agend_cita_presencial == "No" and rec.opportunity_id and rec.opportunity_id.stage_id.name == "Agenda cita virtual":
                crm_stage = self.env["crm.stage"].sudo().search([("name","=","Contactado")],limit=1)
                rec.opportunity_id.stage_id = crm_stage.id
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
            if not rec.opportunity_id:
                partners_opportunity = rec.partner_ids.sudo().filtered(lambda partner: partner.x_studio_enviar_a and partner.opportunity_ids.filtered(lambda opportunity: opportunity.stage_id.name in ["Agenda cita", "Agenda cita virtual"]))
                partners_without = rec.partner_ids.sudo().filtered(lambda partner: partner.x_studio_enviar_a and partner.id != rec.env.user.partner_id.id and partner.opportunity_ids.sudo().filtered(lambda opportunity: opportunity.stage_id.name not in ["Agenda cita", "Agenda cita virtual"]))
                if partners_opportunity:
                    for partner in partners_opportunity:
                        for opportunity in partner.opportunity_ids.sudo().filtered(lambda opportunity: opportunity.stage_id.name in ["Agenda cita", "Agenda cita virtual"]):
                            rec["opportunity_id"] = opportunity.id
                elif partners_without:
                    for partner_without in partners_without:
                        lead_type = partner_without.x_studio_enviar_a
                        lead = {
                            "name": f"{partner_without.name} oportunidad",
                            "partner_id": partner_without.id,
                            "email_from": partner_without.email_formatted,
                            "phone": partner_without.phone,
                            "user_id": partner_without.env.user.id,
                            "expected_revenue": 0,
                            "probability": 0.0,
                            "company_id": rec.env.company.id
                        }
                        if lead_type == "Agenda Cita Presencial":
                            stage = rec.env['crm.stage'].sudo().search([('name', '=', "Agenda cita")], limit=1)
                            lead["stage_id"] = stage.id
                        elif lead_type == "Agenda Cita Virtual":
                            stage = rec.env['crm.stage'].sudo().search([('name', '=', "Agenda cita virtual")], limit=1)
                            lead["stage_id"] = stage.id
                        opportunity = rec.env["crm.lead"].sudo().create(lead)
                        rec["opportunity_id"] = opportunity.id