from odoo import models, fields, api

class ProdShapeList(models.Model):
    _name = 'prod.shape.list'
    _description = 'ProdShapeList'
    _order = 'id desc'


    name = fields.Char('Nombre')
    product_ids = fields.Many2many('product.template')
