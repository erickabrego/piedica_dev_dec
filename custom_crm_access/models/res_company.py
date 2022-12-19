# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    x_crm_access_ids = fields.One2many("crm.access.rule", "company_id", string="Reglas de acceso a crm")

    def get_crm_access_rules(self):
        domain = ['|','|',('team_id','=',False),('team_id','in',self.env.user.mapped('x_crm_team_ids').ids),('company_id','=',False),('company_id','in',self.env.company.mapped('x_crm_access_ids').mapped('company_ids').ids)]
        return domain