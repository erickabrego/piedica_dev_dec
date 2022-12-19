# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import requests
import logging
from pytz import timezone

_logger = logging.getLogger(__name__)


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    x_contact_irina = fields.Char(string="Contacto irina")

    #---------------------------------------Métodos CRUD---------------------------------------------------------

    @api.model
    def create(self, vals_list):
        res = super(CalendarEvent, self).create(vals_list)
        #Se envia mensaje de cita agendada
        res.send_irina_message(template="piedica_confirmacion_cita")
        return res

    def write(self, vals):
        res = super(CalendarEvent, self).write(vals)
        for rec in self:
            #Si la cita se confirma
            if vals.get("x_studio_paciente_confirm_asistencia"):
                if rec.x_studio_paciente_confirm_asistencia:
                    #Se envia mensaje de confirmación
                    rec.send_irina_message(template="piedica_cita_confirmada",parameters=1)
        return res

    #--------------------------------------Métodos de clase------------------------------------------------------

    #Envio de mensajes a Irina
    def send_irina_message(self, template=None, parameters=4, buttons=1):
        for rec in self:
            url = f"https://app.irina.chat/api/v1/messages/send_template"
            token = self.env['ir.config_parameter'].sudo().get_param("irina.token")
            waba = self.env['ir.config_parameter'].sudo().get_param("irina.waba")
            number_id = self.env['ir.config_parameter'].sudo().get_param("irina.number_id")
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
            user_tz = rec.user_id.tz
            #raise ValidationError(rec.start.astimezone(timezone(user_tz))
            #Se obtiene el contacto del paciente o pacientes
            partners = rec.partner_ids.filtered(lambda line: line.x_studio_es_paciente)
            for partner in partners:
                #Se verifica que el paciente tenga celular
                if partner.mobile:
                    mobile_number = rec.format_mobile_number(partner.mobile, partner)
                    components = [{
                            "type": "body",
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": f"{partner.name}"
                                },
                            ]
                        }
                    ]
                    if parameters == 4:
                        components[0]["parameters"].append({
                            "type": "text",
                            "text": f"{rec.x_studio_sucursal or rec.env.company.name}"
                        })
                        components[0]["parameters"].append({
                            "type": "text",
                            "text": f"{rec.user_id.name}"
                        })
                        components[0]["parameters"].append({
                            "type": "text",
                            "text": f"{rec.start.astimezone(timezone(user_tz)).strftime('%d-%b-%Y %I.%M %p')}"
                        })

                    if buttons == 1:
                        buttons_components = {
                            "type": 'button',
                            "sub_type": 'url',
                            "index": '0',
                            "parameters": [
                                {
                                    'type': 'text',
                                    'text': f'{rec.generate_address_url()}'
                                }
                            ]
                        }
                        components.append(buttons_components)
                    else:
                        buttons_components = {
                            "type": 'button',
                            "sub_type": 'quick_reply',
                            "index": '0',
                            "parameters": [
                                {
                                    'type': 'payload',
                                    'payload': '/confirmacion_cita{\"event\":\"CONFIRMATION\"}',
                                    "text": "Confirmar cita"
                                }
                            ]
                        }
                        buttons_components_2 = {
                                "type": 'button',
                                "sub_type": 'quick_reply',
                                "index": '1',
                                "parameters": [
                                    {
                                        'type': 'payload',
                                        'payload': '/reagendar_cita{\"event\":\"RESCHEDULE\"}',
                                        "text": "Reagenda tu cita"
                                    }
                                ]
                            }
                        components.append(buttons_components)
                        components.append(buttons_components_2)

                    message_data = {
                        "to": f"{str(mobile_number).replace(' ', '')}",
                        "waba": waba,
                        "number_id": number_id,
                        "template_name": template,
                        "template_language": "es_mx",
                        "components":components,
                        "contact": {
                            "name": f"{partner.name}",
                            "last_name": ""
                        }
                    }
                    try:
                        response = requests.post(url, json=message_data, headers=headers)
                        content = eval(response.content.decode('UTF-8'))
                        rec.x_contact_irina = content.get("contact_id") if content else False
                        _logger.info("DATOS ENVIADOS A IRINA")
                        _logger.info(message_data)
                        _logger.info("RESPUESTA IRINA")
                        _logger.info(response.content)
                    except Exception as error:
                        _logger.info(error)
                else:
                    raise ValidationError(
                        "El paciente debe de tener un número móvil para comunicarse con él mediante whatsapp.")

    def notify_irina_hours_before(self, events):
        for event in events:
            event.send_irina_message(template="piedica_recordatorio_2_antes")

    def notify_irina_day_before(self, events):
        for event in events:
            event.send_irina_message(template="piedica_recordatorio_24_antes", buttons=2)

    def notify_tips(self):
        for rec in self:
            rec.send_irina_message(template="piedica_confirmacion_cita")

    def generate_address_url(self):
        #Eliminar las tildes de nuestra cadena
        a, b = 'áéíóúüñÁÉÍÓÚÜÑ', 'aeiouunAEIOUUN'
        trans = str.maketrans(a, b)
        #Iniciamos el query de nuestra url
        maps_url = "?q="
        #Obtenemos la dirección de la sucursal
        location = self.appointment_type_id.location or self.location or self.env.company.partner_id.contact_address_complete
        location = "".join(ch for ch in location if ch.isalnum() or str(ch).isspace())
        if location:
            maps_url += str(location).replace(" ", "+")
        maps_url = maps_url.translate(trans)
        return maps_url.strip()

    def format_mobile_number(self, mobile, contact):
        country_code = "52"
        if contact and contact.country_id.phone_code:
            country_code = contact.country_id.phone_code
        if f"+{country_code}" in mobile:
            mobile_number = mobile
        else:
            mobile_number = f"+{country_code}{mobile}"
        return mobile_number
