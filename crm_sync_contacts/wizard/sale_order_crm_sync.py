from odoo import api, fields, models
import requests

class SaleOrderCRMSync(models.TransientModel):
    _name = 'sale.order.crm.sync'
    _description = 'Pedidos de CRM'

    order_id = fields.Many2one(comodel_name="sale.order", string="Venta")
    name = fields.Char(string="Orden", related="order_id.name")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Cliente", related="order_id.partner_id")
    order_ids = fields.One2many("sale.order.crm.sync.line", "order_id", string="Pedidos")

    def search_crm_orders(self):
        endpoint = f"https://crmpiedica.com/api/searchorderpatient.php?id={self.partner_id.id}"
        token = self.env['ir.config_parameter'].sudo().get_param("crm.sync.token")
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(endpoint, headers=headers)
        response_json = response.json()
        print(response_json)
        for order in response_json:
            id_odoo_order = order.get("id_pedido_odoo")
            id_odoo_order = self.env["sale.order"].sudo().search([("name", "=", id_odoo_order)], limit=1)
            if id_odoo_order:
                data = {
                    "id_crm": order.get("id_pedido"),
                    "order_id": self.id,
                }
                order_line = self.env["sale.order.crm.sync.line"].sudo().create(data)
                products = order.get("productos_pedidos")
                if products:
                    # products = products.replace("id_odoo","'id_odoo'")
                    # products = products.replace("'id_odoo':","'id_odoo':''")
                    # products = products.replace("producto:","'producto':'")
                    # products = products.replace("}","'}")
                    # products = eval(products)

                    for product in id_odoo_order.order_line:
                        if product:
                            # product = self.env["product.product"].browse(product.get("id_odoo"))
                            data = {
                                "product_id": product.product_id.id,
                                "product_qty": product.product_qty,
                                "product_uom": product.product_uom.name,
                                "id_order_line": product.id
                            }
                            order_line.product_ids = [(0,0,data)]

    def add_product_lines(self):
        for order in self.order_ids:
            product_lines = order.product_ids.filtered(lambda line: line.add_line)
            for product in product_lines:
                order_line = self.env["sale.order.line"].browse(product.id_order_line.id)
                data = {
                    "product_id": order_line.product_id.id,
                    "product_qty": order_line.product_qty,
                    "insole_size": order_line.insole_size,
                    "design_type": order_line.design_type,
                    "tax_id": order_line.tax_id
                }
                self.order_id.order_line = [(0,0,data)]



