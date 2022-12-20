from odoo import api, fields, models, _

class MergeDeliveries(models.TransientModel):
    _inherit = "merge.deliveries.wizard"

    #Modificamos la preparación de las ordenes agrupadas para dejar ratro de cuales son aquellas transferencias agrupadas
    def prepare_to_merge_deliveries(self):
        res = super(MergeDeliveries, self).prepare_to_merge_deliveries()
        merge_picking = self.env["stock.picking"].sudo().browse(res.get("res_id"))
        if merge_picking:
            merge_picking.x_merge_pickings = self.picking_ids.ids
            merge_picking.origin = ", ".join(self.picking_ids.mapped("origin"))
        return res