from odoo import models, fields, api

class ExamStatusHistory(models.Model):
    _name = 'exam.status.history'
    _description = 'Historial de estatus del estudio médico'
    _order = 'id desc'


    exam_id = fields.Many2one('patient.exam', ondelete='cascade', string='Orden de venta', required=True, readonly=True, help='Estudios del paciente.')
    exam_status_id = fields.Many2one('exam.status', string='Estatus', readonly=True, help='Estatus de los estudios del paciente.')
    date = fields.Datetime('Fecha', readonly=True, help='Fecha y hora de creación del registro.')
