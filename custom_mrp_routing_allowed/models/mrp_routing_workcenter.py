# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MRPRoutingWorkcenter(models.Model):
    _inherit = "mrp.routing.workcenter"

    x_allowed_user_ids = fields.Many2many(comodel_name="res.users", string="Usuarios permitidos")