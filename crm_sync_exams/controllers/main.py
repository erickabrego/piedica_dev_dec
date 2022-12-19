from odoo import http, fields
from odoo.http import Controller, request, route, Response
from odoo.exceptions import UserError


class MainController(Controller):
    @route('/sync-exams', type='json', auth='none')
    def create_exam(self, **kwargs):
        patient_exam_obj = request.env['patient.exam'].sudo()
        result = patient_exam_obj.create_exam(kwargs)

        return result


    @route('/sync-exams/<id>/generate', type='json', auth='none')
    def edit_exam(self, id, **kwargs):
        if not str(id).isnumeric():
            return {
                'status': 'error',
                'message': 'El id del estudio debe ser un valor numérico. Valor introducido: %s' % str(id)
            }

        exam = request.env['patient.exam'].sudo().search([('exam_crm_id', '=', int(id))])

        if not exam:
            return {
                'status': 'error',
                'message': 'No se encontró el estudio con el id %s' % id
            }

        result = exam.to_generated(kwargs)

        return result
