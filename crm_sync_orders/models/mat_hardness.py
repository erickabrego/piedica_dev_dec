from odoo import models, fields

class MatHardness(models.Model):
    _name = 'mat.hardness'
    _description = 'MatHardness'
    _order = 'id desc'


    name = fields.Char('Nombre')
