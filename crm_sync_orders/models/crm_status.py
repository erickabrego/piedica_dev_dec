from odoo import models, fields

class CRMStatus(models.Model):
    _name = 'crm.status'
    _description = 'Estatus de CRM'
    _order = 'id desc'


    code = fields.Integer('Clave')
    name = fields.Char('Nombre')
    portal_label = fields.Char('Nombre en portal')
