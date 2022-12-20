# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class website_seo_redirection(models.Model):
#     _name = 'website_seo_redirection.website_seo_redirection'
#     _description = 'website_seo_redirection.website_seo_redirection'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
