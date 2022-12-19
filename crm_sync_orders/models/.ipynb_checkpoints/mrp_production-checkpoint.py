from datetime import datetime, timedelta

from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    observations = fields.Text(string='Observaciones', compute='_compute_observations')


    @api.depends('procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id')
    def _compute_observations(self):

        for production in self:
            production.observations = ''
            sale_order = production.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id

            if len(sale_order) == 1:
                if sale_order.observations:
                    production.observations = sale_order.observations
