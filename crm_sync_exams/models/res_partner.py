from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    exams_manager = fields.Many2one('res.users', string='Encargado de estudios')
    category_name = fields.Char(related='category_id.name')
