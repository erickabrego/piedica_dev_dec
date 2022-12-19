# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MRPWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    x_allowed_user_ids = fields.Many2many(comodel_name="res.users", string="Usuarios permitidos")