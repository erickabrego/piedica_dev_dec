# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import datetime


class PaymentQuotaEmployee(models.Model):
    _name = 'payment.quota.employee'
    
    name = fields.Char(string='Name', default=lambda x: x._generate_secuencia())
    process_period = fields.Char('Period of Process')
    record_patronal = fields.Char('Record patronal')
    process_date = fields.Date('Process date')
    name_reason_social = fields.Char('Name or reason social')
    activity = fields.Char('Activity')
    state = fields.Selection([('draf', 'Draf'), ('confirmed', 'Confirmed')], default='draf', readonly=True,
                             string="State")
    payment_quota_line_ids = fields.One2many('payment.quota.employee.line', 'payment_quota_id', string='Lines')
    company_id = fields.Many2one('res.company', string='Company', readonly=True,
                                 default=lambda self: self.env.company.id)
    
    def unlink(self):
        for record in self:
            if record.state != 'draf':
                raise UserError(_('Solo solo se puede eliminar en estado Borrador.'))
        return super(PaymentQuotaEmployee, self).unlink()
    
    def _generate_secuencia(self):
        payment_quota_objs = self.search([])
        fecha = datetime.datetime.now()
        anno = str(fecha.year)
        mes = str(fecha.month)
        t = len(payment_quota_objs)
        if t == 0:
            return 'PE/' + anno + '/' + mes + '/' + '000000001'
        else:
            ultimo_record = payment_quota_objs[t - 1]
            sec_num = int(ultimo_record.name.split('/')[3].split('00000000')[1]) + 1
            return 'PE/' + anno + '/' + mes + '/' + '00000000' + str(sec_num)
    
    def importar_fichero(self):
        importar_wizard = {
            'name': 'Import',
            'type': 'ir.actions.act_window',
            'res_model': 'import.payment.quota.employee',
            'view_mode': 'form',
            'target': 'new'
        }
        return importar_wizard
    
    def confirmar(self):
        asiento_obj = self.env['account.move']
        company_obj = self.env['res.company']
        
        for rec in self.payment_quota_line_ids:
            company = company_obj.sudo().search([('name', '=', rec.sucursal)])
            if len(company) > 0:
                line_ids1 = [(5, 0, 0)]
                line_ids2 = [(5, 0, 0)]
                line_ids1.append((0, 0, {'account_id': company.patronal_account_id.id, 'debit': rec.patronal}))
                line_ids1.append((0, 0, {'account_id': company.journal_id.payment_credit_account_id.id, 'name': rec.lic,
                                         'credit': rec.patronal}))
                
                line_ids2.append((0, 0, {'account_id': company.worker_account_id.id, 'debit': rec.worker}))
                line_ids2.append((0, 0, {'account_id': company.journal_id.payment_credit_account_id.id, 'name': rec.lic,
                                         'credit': rec.worker}))
                
                move = asiento_obj.sudo().create({'journal_id': company.journal_id.id, 'line_ids': line_ids1})
                move.post()
                move = asiento_obj.sudo().create({'journal_id': company.journal_id.id, 'line_ids': line_ids2})
                move.post()
            else:
                raise ValidationError(_('Error! There are records that do not have the company.'))
        
        self.write({'state': 'confirmed'})


class PaymentQuotaEmployeeLine(models.Model):
    _name = 'payment.quota.employee.line'
    
    key_code = fields.Char('Key code')
    date = fields.Date('Date')
    days = fields.Integer('Days')
    sdi = fields.Float('SDI')
    lic = fields.Char('Lic.')
    patronal = fields.Float('Patronal')
    worker = fields.Float('Worker')
    subtotal = fields.Float('Subtotal')
    sucursal = fields.Char('Sucursal')
    payment_quota_id = fields.Many2one('payment.quota.employee')
