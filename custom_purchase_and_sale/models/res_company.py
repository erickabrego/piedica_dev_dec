from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    x_is_factory = fields.Boolean(string="Es fábrica?")