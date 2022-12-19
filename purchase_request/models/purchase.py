# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    req_order_id = fields.Many2one('request.order.purchase', 'Request Order')
    department_id = fields.Many2one("hr.department", "Department")

    @api.onchange('req_order_id')
    def _onchange_req_order_id(self):
        if self.req_order_id:
            lines = [(5, 0, 0)]
            products_line = self.req_order_id.order_line
            for product in products_line:
                val = {
                    'product_id': product.product_id.id,
                    'product_qty': product.product_qty,
                    'taxes_id': product.taxes_id.ids,
                    'product_uom': product.product_uom.id,
                    'price_unit': product.price_unit,
                    'name': product.name,
                    'display_type': product.display_type,
                    'account_analytic_id': product.account_analytic_id.id,
                    'analytic_tag_ids': product.analytic_tag_ids.ids
                }
                lines.append((0, 0, val))

            self.order_line = lines
            self.department_id = self.req_order_id.department_id.id if self.req_order_id.department_id else False
            for line in self.order_line:
                price_unit = line.price_unit
                qty = line.product_uom
                line._onchange_quantity()
                line.price_unit = price_unit
                line.product_uom = qty

    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        if 'department_id' in self.env['account.move']._fields:
            invoice_vals['department_id'] = self.department_id.id if self.department_id else False
        invoice_vals['payment_reference'] = ''
        return invoice_vals
