from odoo import models, fields, api
import requests


class StockPicking(models.Model):
    _inherit = 'stock.picking'

#     def write(self, vals):
#         res = super(StockPicking, self).write(vals)
#         for rec in self:
#             if rec.state == "done" and rec.sale_id.folio_pedido:
#                 # Hacemos uso de la API externa para mandar la información del pedido y su etapa para marcar como enviado
#                 url = f"https://crmpiedica.com/api/api.php?id_pedido={rec.sale_id.folio_pedido}&id_etapa=6"
#                 response = requests.put(url)
#                 rec.sale_id.message_post(body=response.content)
#                 crm_status = self.env["crm.status"].search([("code", "=", "6")], limit=1)
#                 if crm_status:
#                     rec.sale_id.write({'estatus_crm': crm_status.id})
#                     rec.sale_id.create_estatus_crm()
#         return res


    def add_qty_done_by_sale_line(self, sale_order_line_id, qty_done):
        self.ensure_one()

        for move in self.move_ids_without_package:
            if move.sale_line_id.id == sale_order_line_id:
                move.sudo().write({'quantity_done': qty_done})

                mrp_done_ids = self.env["mrp.production"].sudo().search([("origin","=",self.sale_id.name)])

                if len(mrp_done_ids) == len(mrp_done_ids.filtered(lambda order_mrp: order_mrp.state == 'done' and order_mrp.p_to_send)):
                    crm_status = self.env["crm.status"].sudo().search([("code", "=", "24")], limit=1)

                    if crm_status:
                        self.sale_id.write({'estatus_crm': crm_status.id})
                        self.sale_id.sudo().create_estatus_crm()

                        url = f"https://crmpiedica.com/api/api.php?id_pedido={self.sale_id.folio_pedido}&id_etapa=1"
                        token = self.env['ir.config_parameter'].sudo().get_param("crm.sync.token")
                        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
                        response = requests.patch(url, headers=headers)
                        self.sale_id.sudo().message_post(body=response.content)

                break
