from odoo import models, fields

class MatMaterialType(models.Model):
    _name = 'mat.material.type'
    _description = 'MatMaterialType'
    _order = 'id desc'


    name = fields.Char('Nombre')
