from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def add_qty_done_by_sale_line(self, sale_order_line_id, qty_done):
        self.ensure_one()

        found = False

        for move in self.move_ids_without_package:
            if move.sale_line_id.id == sale_order_line_id:
                move.write({'quantity_done': qty_done})
                found = True
                break

        if found:
            sucursal_category = self.env['res.partner.category'].search([('name', '=', 'Sucursal')])

            if (sucursal_category) and (sucursal_category[0] not in self.partner_id.category_id):
                print('==========================')
                print('no sucursal')
                print('==========================')
                res = self.button_validate()
                
                
                
