from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MergeDeliveries(models.TransientModel):
    _name = "merge.deliveries.wizard"

    picking_ids = fields.Many2many('stock.picking', string='Deliveries', required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", default=lambda self: self.env.company,
                                 required=True)

    def prepare_to_merge_deliveries(self):

        if self.picking_ids.ids == []:
            raise UserError(_('No delivery to merge'))

        if len(self.picking_ids.ids) == 1:
            raise UserError(_('Single delivery can not be merged'))

        sale_id = self.picking_ids.mapped('sale_id.id')
        # if len(set(sale_id)) is not 1: #popup and confirm
        picking_type = self.picking_ids.mapped('picking_type_id.code')
        partner = self.picking_ids.mapped('partner_id.id')
        states = self.picking_ids.mapped('state')

        if len(set(states)) > 1:
            raise UserError(_('Merge is not allowed for pickings of different state'))

        if len(set(picking_type)) > 1:
            raise UserError(_('Merge is only allowed between same type of deliveries'))

        if len(set(partner)) > 1:
            raise UserError(_('Merge is only allowed between deliveries of same customer'))

        merged_picking = self.picking_ids[0].merge_deliveries(self.picking_ids)

        if merged_picking.state is not 'done':
            merged_picking.do_unreserve()

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'stock.picking',
            'target': 'current',
            'res_id': merged_picking.id
        }










