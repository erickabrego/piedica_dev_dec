from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    insole_size = fields.Char(string='Talla')
    #top_cover_id = fields.Many2one('product.product', string='Top Cover', domain="[('matTopLayer', '=', True), ('qty_available', '>', 0),('is_material','=',True)]")
    top_cover_id = fields.Many2one('product.product', string='Top Cover', domain="[('matTopLayer', '=', True), ('is_material','=',True)]")
    main_layer_id = fields.Many2one('product.product', string='Main Layer', domain="[('matMainLayer', '=', True)]")
    mid_layer_id = fields.Many2one('product.product', string='Mid Layer', domain="[('matMidLayer', '=', True)]")
    design_type = fields.Selection([
        ('1', 'Comfort'),
        ('2', 'Clinical'),
        ('3', 'Medical')
    ], string='Tipo de diseño')
