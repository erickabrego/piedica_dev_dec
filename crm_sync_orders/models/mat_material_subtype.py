from odoo import models, fields

class MatMaterialSubType(models.Model):
    _name = 'mat.material.subtype'
    _description = 'MatMaterialSubType'
    _order = 'id desc'


    name = fields.Char('Nombre')
