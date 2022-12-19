from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    p_is_mto = fields.Boolean(compute='_compute_p_is_mto')


    @api.depends('product_id', 'product_id.route_ids')
    def _compute_p_is_mto(self):
        self.p_is_mto = False

        for move in self:
            product = move.product_id
            product_routes = (product.route_ids + product.categ_id.total_route_ids)

            mto_route = move.warehouse_id.mto_pull_id.route_id
            if not mto_route:
                try:
                    mto_route = self.env['stock.warehouse']._find_global_route('stock.route_warehouse0_mto', _('Make To Order'))
                except UserError:
                    pass

            if mto_route and mto_route in product_routes:
                move.p_is_mto = True
            else:
                move.p_is_mto = False
