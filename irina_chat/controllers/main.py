# -*- coding: utf-8 -*-

from odoo.http import Controller, request, route, Response
import logging
_logger = logging.getLogger(__name__)

class MainController(Controller):

    #Endpoint para obtener ubicación desde irina
    @route('/ubicacion_sucursal', type='json', auth='none')
    def get_irina_location(self, **kwargs):
        #Obtener ubicaciones
        contact_id = kwargs.get("contact_id", None)
        if contact_id:
            event_id = request.env["calendar.event"].sudo().search([("x_contact_irina","=",contact_id)],limit=1)
            if event_id:
                data = {
                    'status': 'success',
                    'content': {
                        'location': event_id.appointment_type_id.location
                    }
                }
            else:
                data = {
                    'status': 'error',
                    'message': f'No existe un evento que esté relacionado al id del contacto {contact_id}.'
                }
        else:
            data = {
                'status': 'error',
                'message': f'Por favor de proporcionar el id del contacto.'
            }

        return data

    #Endpoint para obtener ubicación desde irina
    @route('/confirmar_cita_irina', type='json', auth='none')
    def confirm_event_irina(self, **kwargs):
        _logger.info(kwargs)
        data = {
            'status': 'success',
            'message': 'Hecho'
        }
        return data

