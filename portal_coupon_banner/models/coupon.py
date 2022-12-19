from odoo import models, fields


class Coupon(models.Model):
    _inherit = 'coupon.coupon'

    p_type = fields.Selection([
        ('renovacion', 'Renovación')
    ], string='Tipo de cupón')
