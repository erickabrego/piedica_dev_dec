# -*- coding: utf-8 -*-pack

from odoo import fields, models

class AvailabelCarrier(models.Model):
    _name = "available.carrier"
    _rec_name = "carrier_name"

    carrier_name = fields.Char(string="Available Carrier ", copy=False,help="Available Carrier Name")
    country_code = fields.Char(string="Carrier Country Code",copy=False, help="Country Code")