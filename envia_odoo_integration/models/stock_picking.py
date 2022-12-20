# -*- coding: utf-8 -*-pack
from odoo import models, fields, api, _

class EnviaStockPicking(models.Model):
    _inherit = "stock.picking"

    envia_tracking_url = fields.Text(string="Envia Tracking Url", help="you can track order using this link")
    envia_label = fields.Char(string="Envia Label", help="Envia Shipment Label")
    # envia_parcel_status = fields.Char(string="Envial Parcel Status", help="Status Of Your Parcel")
