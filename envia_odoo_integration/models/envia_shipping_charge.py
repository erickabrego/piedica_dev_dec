# -*- coding: utf-8 -*-pack
from odoo import models, fields

class EnviaShippingCharge(models.Model):
    _name = 'envia.shipping.charge'
    _rec_name = 'envia_service'

    envia_carrier = fields.Char(string="Envia Carrier Name",help="Carrier Name")
    envia_service = fields.Char(string="Envia Service Name", help="Service Name")
    envia_delivery_estimate = fields.Char(string="Envia Delivery Estiate Time", help="Estimate Delivery Time")
    envia_total_price = fields.Char(string="Envia Total Price", help="Total Proice")
    envia_currency = fields.Char(string="Currency", help="Envia Accept Currency")
    sale_order_id = fields.Many2one("sale.order", string="Sales Order")

    def set_service(self):
        self.ensure_one()
        carrier = self.sale_order_id.carrier_id
        self.sale_order_id._remove_delivery_line()
        self.sale_order_id.envia_shipping_charge_id = self.id
        # self.sale_order_id.delivery_price = float(self.envia_total_price)
        self.sale_order_id.carrier_id = carrier.id
        self.sale_order_id.set_delivery_line(carrier, float(self.envia_total_price))