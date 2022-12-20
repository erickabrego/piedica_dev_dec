from odoo import models, fields

class ProdProdUseList(models.Model):
    _name = 'prod.prod.use.list'
    _description = 'ProdProdUseList'
    _order = 'id desc'


    name = fields.Char('Nombre')
    product_ids = fields.Many2many('product.template')
