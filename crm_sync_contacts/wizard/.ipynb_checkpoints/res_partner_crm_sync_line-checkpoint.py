# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartnerCRMSyncLine(models.TransientModel):
    _name = 'res.partner.crm.sync.line'
    _description = 'Linea de sincronización de contactos con CRM'

    name = fields.Char(string="Nombre")
    crm_id = fields.Char(string="Id de paciente")
    gender = fields.Char(string="Sexo")
    birth_date = fields.Date(string="Fecha de nacimiento")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Telefono")
    mobile = fields.Char(string="Celular")
    height = fields.Float(string="Estatura")
    weight = fields.Float(string="Peso")
    template_size = fields.Char(string="Talla del calzado")
    patient_id = fields.Many2one(comodel_name="res.partner.crm.sync", string="Contacto CRM")
    sync_id = fields.Boolean(string="¿Sincronizar ID?")



