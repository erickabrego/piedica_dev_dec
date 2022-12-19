from odoo import api, fields, models,_

class SaleOrderCRMSyncLine(models.TransientModel):
    _name = 'sale.order.crm.sync.line'
    _description = 'Lineas de sincronización de ordenes de venta'

    id_crm = fields.Char("ID pedido")
    order_id = fields.Many2one(comodel_name="sale.order.crm.sync", string="Orden CRM")
    name = fields.Char(string="Venta Odoo", related="order_id.name")
    product_ids = fields.One2many("sale.order.crm.sync.product.line", "order_id", string="Productos")

    def open_product_lines(self):
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_model': 'sale.order.crm.sync.line',
            'name': _("Lineas de pedido Odoo-CRM"),
            'res_id': self.id,
            'views': [(False, 'form')],
        }

class SaleOrderCRMSyncProductLine(models.TransientModel):
    _name = 'sale.order.crm.sync.product.line'
    _description = 'Lineas de productos sincronización de ordenes de venta'

    add_line = fields.Boolean(string="¿Agregar line de producto?")
    product_id = fields.Many2one(comodel_name="product.product", string="Producto")
    description = fields.Char(string="Descripción", related="product_id.name")
    sku = fields.Char(string="SKU", related="product_id.default_code")
    product_qty = fields.Float(string="Cantidad")
    product_uom = fields.Char(string="Unidad de medida")
    order_id = fields.Many2one(comodel_name="sale.order.crm.sync.line", string="Lineas de orden")
    id_order_line = fields.Many2one(comodel_name="sale.order.line", string="Linea de venta")


