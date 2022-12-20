from odoo import models, fields

class MatShoreA(models.Model):
    _name = 'mat.shore.a'
    _description = 'MatShoreA'
    _order = 'id desc'


    value = fields.Char('Valor')
