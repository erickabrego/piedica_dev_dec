from odoo import models, fields

class MatColor(models.Model):
    _name = 'mat.color'
    _description = 'MatColor'
    _order = 'id desc'


    name = fields.Char('Nombre')
    product_ids = fields.Many2many('product.template')
