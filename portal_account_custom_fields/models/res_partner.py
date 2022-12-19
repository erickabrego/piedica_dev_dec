from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    p_age = fields.Integer(string='Edad actual')
    p_occupation = fields.Char(string='Ocupación y/o profesión')
    p_physical_activity = fields.Boolean(string='¿Realiza usted alguna actividad física?')
    p_physical_activity_true = fields.Char(string='¿Cuál?')
    main_complaints = fields.Many2many('patient.complaint', string='Principales molestias')
    other_complaints = fields.Char(string='Otras molestias')
    p_contact_you = fields.Boolean(string='¿Desea que nos comuniquemos con usted?')
    p_birth_date = fields.Date(string='Fecha de nacimiento')
    
    
    p_adult_kid = fields.Selection([
        ('adulto', 'Adulto'),
        ('nino', 'Niño'),
    ], string='Adulto o niño')
    p_hear_about_us = fields.Selection([
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('google', 'Google'),
        ('recomendado_doctor', 'Recomendado Doctor'),
        ('recomendado_paciente', 'Recomendado Paciente'),
        ('otro', 'Otro')
    ], string='¿Cómo se enteró de nosotros?')

    p_hear_about_us_other = fields.Char(string='Especificar')
    p_height = fields.Float(string='Estatura')
    p_weight = fields.Float(string='Peso')
    p_shoe_size = fields.Char(string='Número de calzado')
