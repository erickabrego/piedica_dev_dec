# -*- coding: utf-8 -*-
import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import requests
import logging
_logger = logging.getLogger(__name__)

class CRMConfirmSend(models.TransientModel):
    _name = 'crm.confirm.send'
    _description = 'CRM confirm send'

    sale_order = fields.Many2one('sale.order')

    def send_to_crm(self):
        self.sale_order.write({'p_ask_for_send_to_crm': False})
        self.sale_order.action_confirm()
        response = self._send_data()
        return response

    def _send_data(self):
        url = 'https://crmpiedica.com/api/api.php'
        token = self.env['ir.config_parameter'].sudo().get_param("crm.sync.token")
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        data = self._generate_order_data()
        response = requests.post(url, headers=headers, json=data)

        _logger.info('==================================================')
        _logger.info(data)
        _logger.info('--------------------------------------------------')
        _logger.info(response.status_code)
        _logger.info(response.content)
        _logger.info('==================================================')
        #Envío de información al usuario acerca de la respuesta de la petición
        message = response.content.decode("utf-8")
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Error al crear pedido CRM"),
                'message': message,
                'type': 'warning',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
        if "Error" in message:
            self.sale_order.message_post(body=f"Error al crear pedido en CRM: {message}")
            return notification
        elif response.status_code != 200:
            self.sale_order.message_post(body=f"Error al crear pedido en CRM debido a un error en la petición {response.reason}")
            return notification
        else:
            message_list = message.split(",")
            id_pedido_crm = "".join([str(word) for word in message_list[1] if word.isdigit()])
            id_paciente_crm = "".join([str(word) for word in message_list[2] if word.isdigit()])
            crm_status = self.env["crm.status"].search([("name","=","Control")],limit=1)
            self.sale_order.write({'folio_pedido': id_pedido_crm,'estatus_crm': crm_status.id, 'crm_status_history': [(0,0,{'status':crm_status.id,'date':datetime.date.today()})]})
            #Relacionamos el id_paciente_crm que nos responde la api al contacto si es que no tiene asignado dicho valor
            if not self.sale_order.partner_id.id_crm or self.sale_order.partner_id.id_crm == '':
                self.sale_order.partner_id.write({'id_crm': id_paciente_crm})
            self.sale_order.message_post(body=f"Exito al crear pedido en CRM: {message}")
            notification['params']['title'] = "Pedido creado exitosamente en CRM"
            notification['params']['type'] = 'success'
            return notification

    def _generate_order_data(self):
        order_data = {}

        order_data['tipo_orden'] = 2

        sucursal_category = self.env['res.partner.category'].search([('name', '=', 'Sucursal')])

        if (sucursal_category) and (sucursal_category[0] in self.sale_order.partner_shipping_id.category_id):
            order_data['tipo_orden_envio'] = 1
        else:
            order_data['tipo_orden_envio'] = 2

        order_data['id_pedido'] = self.sale_order.id
        order_data['id_sucursal'] = self.sale_order.branch_id.id
        order_data['id_paciente_cloud'] = 0
        order_data['id_paciente_odoo'] = self.sale_order.partner_id.id
        order_data['id_paciente_crm'] = int(self.sale_order.partner_id.id_crm) or 0

        gender = self.sale_order.partner_id.x_studio_gnero

        order_data['datos_paciente'] = {
            'nombre': str(self.sale_order.partner_id.name).upper(),
            'a_paterno': '',
            'a_materno': '',
            'sexo': str(dict(self.sale_order.partner_id._fields["x_studio_gnero"].selection).get(gender)).upper(), # estatico
            'fecha_nacimiento': self.sale_order.partner_id.x_studio_cumpleaos,
            'email': self.sale_order.partner_id.email,
            'telefono': self.sale_order.partner_id.phone,
            'celular': self.sale_order.partner_id.mobile,
            'estatura': self.sale_order.partner_id.x_studio_altura_cm,
            'peso': self.sale_order.partner_id.x_studio_peso_kgs,
            'id_tallacalzado': float(self.sale_order.partner_id.x_studio_talla),
            'id_sucursal': self.sale_order.branch_id.id,
            "nombre_prescripcion": "",
            "link_prescripcion":""
        }

        order_data['datos_envio'] = {
            'calle': self.sale_order.partner_shipping_id.street_name,
            'colonia': self.sale_order.partner_shipping_id.l10n_mx_edi_colony,
            'municipio': self.sale_order.partner_shipping_id.city_id.name,
            'ciudad': self.sale_order.partner_shipping_id.city_id.name,
            'id_pais': self.sale_order.partner_shipping_id.country_id.name,
            "pais": self.sale_order.partner_shipping_id.country_id.name,
            'id_estado': self.sale_order.partner_shipping_id.state_id.name,
            "estado": self.sale_order.partner_shipping_id.state_id.name,
            'cp': self.sale_order.partner_shipping_id.zip,
            'alias': 'DEFAULT',
        }

        order_data['datos_envio']['datos_pedido'] = {
            'id_estudio': 0,
            'id_tipo_pedido': str(dict(self.sale_order._fields['x_studio_selection_field_waqzv'].selection).get(self.sale_order.x_studio_selection_field_waqzv)).upper(), # estatico
            'id_tipo_disenio': 0,
            'observaciones': self.sale_order.observations,
            'id_pedido_odoo': str(self.sale_order.name).upper(),
            'id_pedido_cloud': 0,
            "nombre_estudio_cloud": "",
            "link_estudio_cloud": "",
            'datos_productos_pedidos': [],
        }

        for line in self.sale_order.order_line.filtered(lambda line: 'Fabricar' in line.product_id.route_ids.mapped('name') and line.product_uom_qty == 1):
            mrp_order = self.env['stock.move'].search([('sale_line_id', '=', line.id)]).created_production_id

            #Marcar como hecho fabricaciones hijas
            if mrp_order:
                mrp_childs = mrp_order._get_children()
                for mrp_child in mrp_childs:
                    mrp_child.update({"qty_producing": mrp_child.product_qty})
                    mrp_child._set_qty_producing()
                    mrp_child.sudo().button_mark_done()
            mrp_order_id = mrp_order.id if mrp_order else None

            order_data['datos_envio']['datos_pedido']['datos_productos_pedidos'].append({
                'id_producto': line.product_id.id,
                'cantidad': line.product_uom_qty,
                'id_recubrimiento': line.top_cover_id.id or 0,
                'id_material': 0,
                'id_disenio': int(line.design_type),
                'id_mo': mrp_order_id,
                'nombre_mo': mrp_order.name
                #'id_QR': mrp_order_id,
            })
        order_data = self._validate_order_data(order_data)
        return order_data


    def _validate_order_data(self, data):
        order_data = data
        sucursal_category = self.env['res.partner.category'].search([('name', '=', 'Sucursal')])

        # Datos de la orden
        if not order_data['datos_envio']['datos_pedido']['observaciones']:
            order_data['datos_envio']['datos_pedido']['observaciones'] = ''

        # _Datos del paciente
        missing_data = []

        if not order_data['datos_paciente']['nombre']:
            missing_data.append('nombre')
        else:
            order_data['datos_paciente']['nombre'] = order_data['datos_paciente']['nombre'].upper()

        if not order_data['datos_paciente']['fecha_nacimiento']:
            missing_data.append('fecha de nacimiento')
        else:
            order_data['datos_paciente']['fecha_nacimiento'] = order_data['datos_paciente']['fecha_nacimiento'].strftime('%Y-%m-%d')

        if not order_data['datos_paciente']['email']:
            missing_data.append('email')
        else:
            order_data['datos_paciente']['email'] = order_data['datos_paciente']['email'].upper()

        if not order_data['datos_paciente']['telefono']:
            order_data['datos_paciente']['telefono'] = ''

        if not order_data['datos_paciente']['celular']:
            if (sucursal_category) and (sucursal_category[0] not in self.sale_order.partner_shipping_id.category_id):
                missing_data.append('celular')
            else:
                order_data['datos_paciente']['celular'] = ''

        if not order_data['datos_paciente']['estatura']:
            missing_data.append('estatura')

        if not order_data['datos_paciente']['peso']:
            missing_data.append('peso')

        if not order_data['datos_paciente']['id_tallacalzado']:
            missing_data.append('calzado')

        if missing_data:
            raise UserError('Faltan los siguientes datos del paciente: %s' % ', '.join(missing_data))

        # Datos del envío
        if not order_data['datos_envio']['calle']:
            missing_data.append('calle')
        else:
            order_data['datos_envio']['calle'] = order_data['datos_envio']['calle'].upper()

        if not order_data['datos_envio']['colonia']:
            missing_data.append('colonia')
        else:
            order_data['datos_envio']['colonia'] = order_data['datos_envio']['colonia'].upper()

        if not order_data['datos_envio']['municipio']:
            missing_data.append('municipio')
        else:
            order_data['datos_envio']['municipio'] = order_data['datos_envio']['municipio'].upper()

        if not order_data['datos_envio']['ciudad']:
            missing_data.append('ciudad')
        else:
            order_data['datos_envio']['ciudad'] = order_data['datos_envio']['ciudad'].upper()

        if not order_data['datos_envio']['id_pais']:
            missing_data.append('id_pais')
        else:
           order_data['datos_envio']['id_pais'] = order_data['datos_envio']['id_pais'].upper()

        if not order_data['datos_envio']['id_estado']:
            missing_data.append('id_estado')
        else:
           order_data['datos_envio']['id_estado'] = order_data['datos_envio']['id_estado'].upper()

        if not order_data['datos_envio']['cp']:
            missing_data.append('codigo postal')
        else:
            order_data['datos_envio']['cp'] = order_data['datos_envio']['cp'].upper()

        if missing_data:
            raise UserError('Faltan los siguientes datos del envío: %s' % ', '.join(missing_data))

        # Comprueba si el producto es custom
        for line in self.sale_order.order_line:
            if line.product_id.is_custom:
                if not line.top_cover_id:
                    raise UserError('Falta agregar el Top Cover para el producto custom %s' % line.product_id.name)

                if not line.top_cover_id:
                    raise UserError('Falta agregar el Main Layer para el producto custom %s' % line.product_id.name)

                if not line.top_cover_id:
                    raise UserError('Falta agregar el Mid Layer para el producto custom %s' % line.product_id.name)

        # Convierte la estructura a como se maneja en CRM (Objetos dentro de arreglos)
        order_data['datos_paciente'] = [order_data['datos_paciente']]
        order_data['datos_envio']['datos_pedido'] = [order_data['datos_envio']['datos_pedido']]
        order_data['datos_envio'] = [order_data['datos_envio']]
        order_data = [order_data]

        return order_data
