from odoo import models, fields

class ProdMaterialSubType(models.Model):
    _name = 'prod.material.subtype'
    _description = 'ProdMaterialSubType'
    _order = 'id desc'


    name = fields.Char('Nombre')
