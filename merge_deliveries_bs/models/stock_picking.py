from odoo import fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_merged = fields.Boolean(string="Is Merged")
    merged_delivery = fields.Boolean(string="Is Merged delivery")

    def select_deliveries_to_merge(self):
        context = {
            'default_company_id': self.env.company.id,
            'default_picking_ids': [(6, 0, [r.id for r in self])]
        }

        return {
            'name': 'merge deliveries',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'merge.deliveries.wizard',
            'target': 'new',
            'context': context
        }

    def merge_deliveries(self, pickings):
        names = pickings.mapped('name')
        weight = sum(pickings.mapped('shipping_weight'))
        new_picking = self.copy({
            'move_lines': [],
            'name': ','.join(names)
        })

        sale_id = self.sale_id

        move_ids = []
        move_line_ids = []
        for picking in pickings:
            for move in picking.move_lines:
                move_ids.append(move.id)
                move_line_ids += move.move_line_ids.mapped('id')

        new_picking.write({"move_lines": [(6, 0, move_ids)]})
        new_picking.write({"move_line_ids_without_package": [(6, 0, move_line_ids)]})

        for picking in pickings:
            picking.sale_id = sale_id
            picking.is_merged = True
            picking.state = 'cancel'
            picking.message_post(
                body=_('This transfer has been merged with %s .') % (
                    new_picking.name))

        new_picking.shipping_weight = weight
        new_picking.merged_delivery = True

        return new_picking
