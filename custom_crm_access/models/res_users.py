# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    x_crm_team_ids = fields.Many2many(comodel_name="crm.team", string="Equipos de venta")

    def write(self,vals):        
        res = super(ResUsers,self).write(vals)
        if vals.get('x_crm_team_ids'):
            self.env['ir.rule'].clear_cache()
        return res