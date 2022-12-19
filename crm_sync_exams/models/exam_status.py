from odoo import models, fields, api

class ExamStatus(models.Model):
    _name = 'exam.status'
    _description = 'Estatus del estudio médico'
    _order = 'id desc'


    name = fields.Char('Nombre')
    code = fields.Char('Clave')
