from odoo import api, fields, models
import requests

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_merge_pickings = fields.Char(string="Transferencias agrupadas")

    #Validamos y obtenemos si la transferencia fue hecha por agrupación y si estos traslados contienen ordenes de venta
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        #Identificamos si se tienen ordenes agrupadadas
        if self.x_merge_pickings:
            #Se convierte en lista los ids de las ordenes agrupadas con la finalidad de buscarlas en la BD
            picking_ids = eval(str(self.x_merge_pickings))
            for picking in picking_ids:
                picking_id = self.env["stock.picking"].sudo().browse(picking)
                #Se obtiene la venta de está transferencia
                sale_id = self.env["sale.order"].sudo().search([("name","=",picking_id.origin)],limit=1)
                if sale_id and sale_id.folio_pedido:
                    #Hacemos uso de la api a CRM para marcar como enviado dicha transferencia
                    url = f"https://crmpiedica.com/api/api.php?id_pedido={sale_id.folio_pedido}&id_etapa=6"
                    token = self.env['ir.config_parameter'].sudo().get_param("crm.sync.token")
                    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
                    

                    # no. seguimiento
                    if picking_id.carrier_tracking_ref:
                        url += '&guia_rastreo=' + picking_id.carrier_tracking_ref

                    # transportista
                    if picking_id.carrier_id:
                        url += '&transportista=' + picking_id.carrier_id.name

                    crm_status = self.env["crm.status"].sudo().search(['|', ('name', '=', 'Enviado'), ("code", "=", "6")], limit=1)
                    if not crm_status.id in sale_id.crm_status_history.mapped("status.id"):
                        response = requests.patch(url, headers=headers)

                        #Agregamos el estatus en la orden de venta y su historial
                        if sale_id.x_branch_order_id:
                            self.send_crm_status_factory(sale_id.x_branch_order_id, response, crm_status)
                            self.send_crm_status_factory(sale_id, response, crm_status)
                        else:
                            factory_order = self.env["sale.order"].sudo().search([("x_branch_order_id.id", "=", sale_id.id)], limit=1)
                            if factory_order:
                                self.send_crm_status_factory(factory_order, response, crm_status)
                            self.send_crm_status_factory(sale_id, response, crm_status)
        return res

    def send_crm_status_factory(self, sale_id, response, crm_status):
        sale_id.sudo().message_post(body=response.content)
        sale_id.sudo().write({'estatus_crm': crm_status.id})
        sale_id.sudo().create_estatus_crm()
