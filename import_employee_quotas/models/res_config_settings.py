# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"
    
    patronal_account_id = fields.Many2one('account.account', string="Patronal account")
    worker_account_id = fields.Many2one('account.account', string="Worker account")
    journal_id = fields.Many2one('account.journal', string="Journal")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    patronal_account_id = fields.Many2one('account.account', 'Patronal account',
                                          related='company_id.patronal_account_id', readonly=False)
    worker_account_id = fields.Many2one('account.account', 'Worker account', related='company_id.worker_account_id',
                                        readonly=False)
    journal_id = fields.Many2one('account.journal', 'Journal', related='company_id.journal_id',
                                 readonly=False)
    
    @api.model
    def create(self, vals):
        self.env.company.write({
            'patronal_account_id': vals.get('patronal_account_id') or self.env.company.patronal_account_id,
            'worker_account_id': vals.get('worker_account_id') or self.env.company.worker_account_id,
            'journal_id': vals.get('journal_id') or self.env.company.journal_id,

        })
        vals.pop('patronal_account_id', None)
        vals.pop('patronal_account_id', None)
        vals.pop('patronal_account_id', None)
        return super().create(vals)
