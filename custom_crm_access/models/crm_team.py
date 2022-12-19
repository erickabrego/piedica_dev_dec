# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CRMTeam(models.Model):
    _inherit = 'crm.team'

    x_company_ids = fields.Many2many(comodel_name="res.company", string="Compañías")


