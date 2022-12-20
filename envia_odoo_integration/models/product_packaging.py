from odoo import fields, models, api


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'
    package_carrier_type = fields.Selection(selection_add=[("envia", "Envia")],
                                            ondelete={'envia': 'set default'})