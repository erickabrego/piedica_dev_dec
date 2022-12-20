from odoo.exceptions import UserError
from odoo import fields, models, api
from datetime import date, datetime


class AccountIncome(models.Model):
    _name = 'account.income'
    _inherit = ['mail.thread', 'mail.activity.mixin', ]
    _description = 'Income Customization'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.credit_account_id = self.product_id.property_account_income_id.id if self.product_id.property_account_income_id else self.product_id.categ_id.property_account_income_categ_id.id

    @api.depends("amount")
    def _compute_total(self):
        for record in self:
            record.total = record.amount
            record.write({'total_amount': record.total})

    name = fields.Char('Description', readonly=True, states={'draft': [('readonly', False)]})
    code = fields.Char()
    income_date = fields.Datetime('Income date', default=lambda self: fields.Datetime.now(), readonly=True,
                                  states={'draft': [('readonly', False)]})
    product_id = fields.Many2one('product.template', 'Product', readonly=True, states={'draft': [('readonly', False)]},
                                 tracking=True)
    amount = fields.Float('Amount', readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    credit_account_id = fields.Many2one('account.account', 'Credit account', readonly=True,
                                        states={'draft': [('readonly', False)]}, tracking=True)
    payment_method_id = fields.Many2one('account.journal', 'Payment method', tracking=True,
                                        help='Payment method or Account journal, usually with cash type.',
                                        readonly=True,
                                        states={'draft': [('readonly', False)]})

    confirm_move_id = fields.Many2one('account.move', 'Confirm move',
                                      help='Move generated when pressing confirm button',
                                      readonly=True, states={'draft': [('readonly', False)]})
    cancel_move_id = fields.Many2one('account.move', 'Cancel move', help='Move generated when pressing cancel button')
    notes = fields.Html(states={'cancelled': [('readonly', True)]}, tracking=True)
    state = fields.Selection([('draft', 'Created'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], 'State',
                             default='draft', tracking=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company,
                                 tracking=True)
    refund_income = fields.Boolean(string="Refund income?", default=False)

    total = fields.Float(string="Total", compute="_compute_total")
    total_amount = fields.Float(string="Monto total")
    account_analytic_id = fields.Many2one("account.analytic.account", string="Account analytic", readonly=True,
                                          states={'draft': [('readonly', False)]})
    account_analytic_tag_id = fields.Many2one("account.analytic.tag", string="Analytic tag", readonly=True,
                                              states={'draft': [('readonly', False)]})
    account_analytic_line_id = fields.Many2one("account.analytic.line", string="Move analytic", readonly=True,
                                               states={'draft': [('readonly', False)]})

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('account.income.seq')
        res = super(AccountIncome, self).create(vals)
        return res

    def set_confirmed(self):
        for record in self:
            record.sudo().generate_account_move_confirm()
            if self.account_analytic_id:
                record.sudo().generate_analytic_move_confirm()
            record.write({'state': 'confirmed'})

    def set_cancelled(self):
        for record in self:
            move = record.confirm_move_id._reverse_moves(default_values_list=[], cancel=True)
            record.cancel_move_id = move.id
            if record.account_analytic_line_id:
                self.account_analytic_line_id.unlink()
            record.write({'state': 'cancelled'})

    def set_draft_again(self):
        self.write({'state': 'draft'})

    def unlink(self):
        if self.state not in ['draft']:
            raise UserError('You can only delete records in Draft state')
        return super(AccountIncome, self).unlink()

    def generate_account_move_confirm(self):
        move_data = {
            "journal_id": self.payment_method_id.id,
            "ref": self.name,
            "date": self.income_date,
            "state": "draft",
        }
        lines = [(0, 0, {
            "partner_id": False,
            "account_id": self.credit_account_id.id,
            "name": self.name,
            "debit": 0.00,
            "credit": abs(self.amount),
        },), (0, 0, {
            "account_id": self.payment_method_id.payment_debit_account_id.id,
            "name": self.name,
            "debit": abs(self.amount),
            "credit": 0.00,
        },
              )]

        move_data.update({"line_ids": lines})
        move = self.env["account.move"].create(move_data)
        move.write({"state": "posted"})
        self.write({"confirm_move_id": move.id})
        return True

    def generate_analytic_move_confirm(self):
        tag_id = [self.account_analytic_tag_id.id] if self.account_analytic_tag_id else False
        val = {
            'name': self.name,
            'tag_ids': tag_id,
            'account_id': self.account_analytic_id.id,
            'date': date.today(),
            'amount': self.total,
            'unit_amount': 1,
            'product_id': self.env["product.product"].search([('product_tmpl_id', '=', self.product_id.id)],
                                                             limit=1).id,
            'move_id': self.confirm_move_id.line_ids[0].id
        }
        move_id = self.env["account.analytic.line"].create(val)
        self.write({'account_analytic_line_id': move_id.id})
