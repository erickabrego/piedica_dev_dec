# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("invoice_count", "invoice_ids.amount_residual")
    def _compute_amount_pending(self):
        for order in self:
            amount_pending = 0.0
            if len(order.invoice_ids) > 0:
                amount_pending = sum(order.invoice_ids.mapped("amount_residual"))
            order.amount_pending = amount_pending
            order.amount_aux =order.amount_pending
            order.write({'amount_pending': order.amount_pending})

    amount_pending = fields.Float(string="Amount pending", store=True, compute="_compute_amount_pending", tracking=4)
    amount_aux = fields.Float(string="Amount aux", compute="_compute_amount_pending")