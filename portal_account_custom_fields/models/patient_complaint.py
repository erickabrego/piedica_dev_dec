from odoo import models, fields, api

class StatusHistory(models.Model):
    _name = 'patient.complaint'
    _description = 'Molestia del paciente'
    _order = 'id desc'


    name = fields.Char(string='Nombre')
    patient_id = fields.Many2many('res.partner', string='Paciente')
