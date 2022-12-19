from odoo import models, fields

class ProdProductionType(models.Model):
    _name = 'prod.production.type'
    _description = 'prodProductionType'
    _order = 'id desc'


    name = fields.Char('Nombre')
