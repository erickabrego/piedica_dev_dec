# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CRMAccessRule(models.Model):
    _name = 'crm.access.rule'
    _description = 'Reglas de acceso a crm'

    name = fields.Char(string="Nombre", compute="_get_name_rule")
    company_id = fields.Many2one(comodel_name="res.company", string="Compañía")
    company_ids = fields.Many2many(comodel_name="res.company", string="Compañías permitidas")

    def write(self,vals):
        res = super(CRMAccessRule,self).write(vals)
        self.env['ir.rule'].clear_cache()
        return res

    @api.depends("company_id")
    def _get_name_rule(self):
        for rec in self:
            rec.name = f"Acceso a CRM para {rec.company_id.name}"
    

