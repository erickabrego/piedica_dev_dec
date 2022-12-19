# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    @api.depends("invoice_count", "invoice_ids.amount_residual")
    def _compute_amount_pending(self):
        for order in self:
            amount_pending = 0.0
            if len(order.invoice_ids) > 0:
                amount_pending = sum(order.invoice_ids.mapped("amount_residual"))
            order.amount_pending = amount_pending
            order.amount_aux = order.amount_pending
            order.write({'amount_pending': order.amount_pending})
    
    @api.onchange("partner_id")
    def _onchange_partner_patient(self):
        if self.partner_id:
            self.patient = True if self.partner_id.x_studio_es_paciente else False
            if self.patient:
                self.how_contact = self.partner_id.x_studio_cmo_nos_contacta or False
                if self.how_contact == 'Internet':
                    self.medium = self.partner_id.x_studio_medio or False
                    self.valor_count = 1
                elif self.how_contact == 'Médico / Especialista':
                    self.doctor_related = self.partner_id.x_studio_medico.name or False
                    self.valor_count = 2
                elif self.how_contact == 'Recomendado paciente':
                    self.patient_recommends_it = self.partner_id.x_studio_nombre_del_paciente_que_lo_recomienda.name or False
                    
                    self.valor_count = 3
                else:
                    self.other_media = self.partner_id.x_studio_medio_otro or False
                    self.valor_count = 4
    
    amount_pending = fields.Float(string="Amount pending", store=True, compute="_compute_amount_pending", tracking=4)
    amount_aux = fields.Float(string="Amount aux", compute="_compute_amount_pending")
    
    patient = fields.Boolean("Paciente")
    how_contact = fields.Char(string="Cómo nos contacta")
    
    patient_recommends_it = fields.Char(string="Paciente que lo recomienda")
    other_media = fields.Char(string="Otros medios")
    medium = fields.Char(string="Medio")
    doctor_related = fields.Char(string="Doctor relacionado")
    valor_count = fields.Integer(string="Valor del campo")
    
    def update_sale_order(self):
        sale_orders_patient = self.search([]).filtered(lambda so: so.partner_id.x_studio_es_paciente)
        for so in sale_orders_patient:
            print("Update SO", so.name)
            so._onchange_partner_patient()
