from odoo import http, fields
from odoo.http import Controller, request, route, Response
from odoo.exceptions import UserError
import json
import logging
_logger = logging.getLogger(__name__)


class MainController(Controller):

    # Endpoint obtener pacientes
    @route('/get-patients/<name>', type='http', auth='none')
    def get_patients(self, name, **kwargs):
        # Obtener pacientes
        patients = request.env['res.partner'].sudo().search(
            [("x_studio_es_paciente", "=", True), ("name", "like", str(name)), ("id_crm", "=", False)])
        patients_list = []
        response = [{'pacientes': patients_list}]
        for patient in patients:
            data = {
                "nombre": patient.name,
                "direccion": str(patient._display_address(False)).replace("\n"," "),
                "correo": patient.email if patient.email else "",
                "nacimiento": patient.x_studio_cumpleaos.strftime("%Y-%m-%d") if patient.x_studio_cumpleaos else "",                
		        "id": patient.id
            }
            response[0]["pacientes"].append(data)
        _logger.info(response)
        return json.dumps(response, indent=2)

    #Endpoint actualizar id de crm
    @route('/update-crm-id/<int:id>', type='json', auth='public')
    def update_crm_id(self, id, **kwargs):             
        patient = request.env['res.partner'].sudo().search([("id", "=", int(id))], limit=1)
        if patient:        
            result = patient.update_crm_id(kwargs)
            return result
        else:
            return {
                'status': 'error',
                'message': f'El id {id} no se encuentra en la base de datos'
            }   
        
    @route('/create-crm-contact', type='json', auth='public')
    def create_crm_contact(self,**kwargs):
        patient = request.env["res.partner"]
        _logger.info(patient)
        result = patient.create_crm_contact(kwargs)
        return result