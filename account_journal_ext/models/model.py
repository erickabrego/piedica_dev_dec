# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.onchange('is_default_journal')
    def onchange_journal_default(self):
        if self.is_default_journal:
            if any(self.env['account.journal'].search([('type','=','sale'),('is_default_journal','=',True),('company_id','=', self.company_id.id)])):
               raise UserError(_('Solo puede tener un Diario por empresa como predeterminado.'))

    is_default_journal = fields.Boolean('Diario predeterminado')

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _get_default_journal(self):
        default_journal = super(AccountMove, self)._get_default_journal()
        aux = self.env['account.journal'].search([('type','=','sale'),('company_id','=', self.env.company.id)])
        journal_def = aux.filtered(lambda x: x.is_default_journal)
        if journal_def:
            journal = journal_def[0]
        else:
            journal = default_journal
        return journal