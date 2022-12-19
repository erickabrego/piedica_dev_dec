# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    x_campaign_id = fields.Many2one(comodel_name="utm.campaign", string="Campaña")
    x_medium_id = fields.Many2one(comodel_name="utm.medium", string="Media")
    x_source_id = fields.Many2one(comodel_name="utm.source", string="Origen")

    # #Se da de alta una oportunidad al momento de crear contacto
    # @api.model
    # def create(self, vals_list):
    #     res = super(ResPartner, self).create(vals_list)
    #     try:
    #         lead_type = res.x_studio_enviar_a
    #         campaign_id = res.x_campaign_id
    #         medium_id = res.x_medium_id
    #         source_id = res.x_source_id
    #         if lead_type:
    #             lead = {
    #                 "name": f"{res.name} oportunidad",
    #                 "partner_id": res.id,
    #                 "email_from": res.email_formatted,
    #                 "phone": res.phone,
    #                 "user_id": res.env.user.id,
    #                 "expected_revenue": 0,
    #                 "probability": 0.0,
    #                 "company_id": res.env.company.id
    #             }
    #             if lead_type == "Agenda Cita Presencial":
    #                 stage = res.env['crm.stage'].sudo().search([('name', '=', "Agenda cita")], limit=1)
    #                 lead["stage_id"] = stage.id
    #                 lead["campaign_id"] = campaign_id.id
    #                 lead["medium_id"] = medium_id.id
    #                 lead["source_id"] = source_id.id
    #             elif lead_type == "Agenda Cita Virtual":
    #                 stage = res.env['crm.stage'].sudo().search([('name', '=', "Agenda cita virtual")], limit=1)
    #                 lead["stage_id"] = stage.id
    #                 lead["campaign_id"] = campaign_id.id
    #                 lead["medium_id"] = medium_id.id
    #                 lead["source_id"] = source_id.id
    #             res.env["crm.lead"].sudo().create(lead)
    #     except Exception as e:
    #         _logger.info(e)
    #     return res
