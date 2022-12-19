from odoo import models, fields, api
import requests

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # Indice de la operación en progreso en la lista "workorder_ids"
    current_operation_index = fields.Integer(default=-1)

    p_to_send = fields.Boolean(default=False)
    p_current_operation = fields.Char(string='Etapa', compute='_compute_p_current_operation')


    def _compute_p_current_operation(self):
        for production in self:
            if production.p_to_send:
                production.p_current_operation = 'Enviado'
            elif production.current_operation_index == -1:
                production.p_current_operation = 'Aún sin empezar'
            else:
                production.p_current_operation = production.workorder_ids[production.current_operation_index].name


    def get_qrcode_line_data(self):
        self.ensure_one()

        workorders = []

        for workorder in self.workorder_ids:
            wo = {
                'id': workorder.id,
                'name': workorder.name,
                'state': workorder.state,
                'duration_expected': workorder.duration_expected,
                'duration': workorder.duration
            }

            workorders.append(wo)

        product = {
            'id': self.product_id.id,
            'name': self.product_id.name
        }

        components = []

        for component in self.move_raw_ids:
            c = {
                'id': component.id,
                'product_id': {
                    'id': component.product_id.id,
                    'name': component.product_id.name
                }
            }

            components.append(c)

        insole_size = self.procurement_group_id.mrp_production_ids.move_dest_ids.sale_line_id.insole_size

        order = {
            'id': self.id,
            'name': self.name,
            'workorder_ids': workorders,
            'product_id': product,
            'move_raw_ids': components,
            'observations': self.observations,
            'current_operation_index': self.current_operation_index,
            'insole_size': insole_size,
            'p_to_send': self.p_to_send
        }

        return order


    def operations_next_stage(self):
        self.ensure_one()

        for workorder in self.workorder_ids:
            if workorder.state == 'ready':
                workorder.button_start()
                #self.increment_operation_index()

                return {
                    'status': 'info',
                    'order': self.name,
                    'message': 'Operacion <b>%s</b> iniciada' % workorder.name
                }

            elif workorder.state == 'progress':
                result = workorder.try_to_finish_from_scan()

                # El método button_finish de mrp.workorder debería devolver True.
                # Si result no es True, entonces button_finish no se ejecutó
                if result != True:
                    result['order'] = self.name

                    return result

                # La orden pasará automáticamente a hecho cuando se hayan
                # terminado todas las etapas
                if self.state == 'to_close':
                    self.button_mark_done()

                return {
                    'status': 'success',
                    'order': self.name,
                    'message': ('Operacion <b>%s</b> terminada' % workorder.name)
                }

        
        if (self.state == 'done') and (not self.p_to_send):
            delivery_order = self.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.picking_ids

            if len(delivery_order) == 1:
                self.write({'p_to_send': True})
                sale_line = self.procurement_group_id.mrp_production_ids.move_dest_ids.sale_line_id
                mrp_done_ids = self.env["mrp.production"].search([("origin","=",sale_line.order_id.name)])
                delivery_order.add_qty_done_by_sale_line(sale_line.id, self.qty_producing)    
                
                if len(mrp_done_ids) == len(mrp_done_ids.filtered(lambda order_mrp: order_mrp.state == 'done' and order_mrp.p_to_send)):                    
                    #Hacemos uso de la API externa para mandar la información del pedido y su etapa para marcar como enviado
                    url = f"https://crmpiedica.com/api/api.php?id_pedido={sale_line.order_id.folio_pedido}&id_etapa=6"
                    response = requests.put(url)
                    sale_line.order_id.message_post(body=response.content)


                return {
                    'status': 'success',
                    'order': self.name,
                    'message': 'La orden ha sido marcada para ser enviada'
                }

        return {
            'status': 'warning',
            'order': self.name,
            'message': 'No hay ninguna operación pendiente en la orden'
        }


    def increment_operation_index(self):
        self.ensure_one()

        self.current_operation_index += 1
