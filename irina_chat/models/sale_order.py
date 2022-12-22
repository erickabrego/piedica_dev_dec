from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_12_months_renewal_sent = fields.Boolean(string="Renovación después de 12 meses")
    x_is_renewal = fields.Boolean(string="¿Plantillas renovadas?")

    def send_irina_message(self, events):
        pass