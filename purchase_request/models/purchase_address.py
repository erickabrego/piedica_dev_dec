# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PurchaseAddress(models.Model):
    _name = "purchase.address"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Lugar de entrega'

    name = fields.Char('Nombre')
    street = fields.Char('Calle 1')
    num_int = fields.Char('Num. Exterior')
    num_ext = fields.Char('Num. Interior')
    colony = fields.Char('Colonia')
    city = fields.Char('Ciudad')
    state_id = fields.Many2one('res.country.state', 'Estado')
    cp = fields.Char('C.P.')
    country_id = fields.Many2one('res.country', 'País')
    company_id = fields.Many2one('res.company', 'Empresa', default=lambda self: self.env.user.company_id.id)
    description = fields.Text('Descripción')
