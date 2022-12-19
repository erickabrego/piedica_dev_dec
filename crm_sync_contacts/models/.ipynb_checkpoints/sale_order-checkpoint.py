from odoo import api, fields, models,_

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def open_crm_orders(self):
        sale_order = self.env["sale.order.crm.sync"]
        data = {"order_id": self.id,}
        order_id = sale_order.sudo().create(data)
        order_id.search_crm_orders()

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_model': 'sale.order.crm.sync',
            'name': _("Pedidos Odoo-CRM"),
            'res_id': order_id.id,
            'views': [(False, 'form')],
        }