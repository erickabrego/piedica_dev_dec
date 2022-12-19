from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    exams_email = fields.Char('Email estudios')
    category_name = fields.Char(related='category_id.name')
