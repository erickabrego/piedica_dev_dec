from datetime import datetime, timedelta

from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    observations = fields.Text(string='Observaciones', compute='_compute_observations')
    p_design_link = fields.Char(string="Liga de plantilla")
    client_id = fields.Many2one('res.partner', string='Cliente', compute='_compute_client_id', store=True)
    folio_pedido = fields.Char('Folio del pedido', readonly=True, copy=False, compute='_compute_folio_pedido', store=True)

    @api.depends('procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id')
    def _compute_observations(self):

        for production in self:
            production.observations = ''
            sale_order = production.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id

            if len(sale_order) == 1:
                if sale_order.observations:
                    production.observations = sale_order.observations

    @api.depends('procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id')
    def _compute_client_id(self):
        for production in self:
            sale_order = production.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id

            if len(sale_order) == 1:
                if sale_order.observations:
                    production.client_id = sale_order.partner_id

    @api.depends('procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id')
    def _compute_folio_pedido(self):
        for production in self:
            sale_order = production.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id

            if len(sale_order) == 1:
                if sale_order.observations:
                    production.folio_pedido = sale_order.folio_pedido
