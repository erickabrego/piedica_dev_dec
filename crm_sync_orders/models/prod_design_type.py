from odoo import models, fields

class ProdDesignType(models.Model):
    _name = 'prod.design.type'
    _description = 'ProdDesignType'
    _order = 'id desc'


    name = fields.Char('Nombre')
    product_ids = fields.Many2many('product.template')
