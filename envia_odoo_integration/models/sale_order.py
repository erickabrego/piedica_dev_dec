# -*- coding: utf-8 -*-pack
from odoo import models, fields, api, _

from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    envia_shipping_charge_ids = fields.One2many('envia.shipping.charge',"sale_order_id", string="Envia Rate Matrix")
    envia_shipping_charge_id = fields.Many2one("envia.shipping.charge", string="Envia Service",
                                                help="This Method Is Use Full For Generating The Label", copy=False)


