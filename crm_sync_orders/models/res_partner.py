from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    id_crm = fields.Char('ID CRM')
