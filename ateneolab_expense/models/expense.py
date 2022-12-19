from odoo.exceptions import UserError
from odoo import fields, models, api
from datetime import date, datetime


class AccountExpense(models.Model):
    _name = 'account.expense'
    _inherit = ['mail.thread', 'mail.activity.mixin', ]
    _description = 'Expenses Customization'

    @api.onchange('refund_expense')
    def _onchange_refund_expense(self):
        if self.refund_expense:
            tax_acc = self.env["config.expense"].search([], limit=1)
            if tax_acc:
                self.tax_account_id = tax_acc.tax_account_refund_id.id
            else:
                self.tax_account_id = False

            if self.product_id:
                if self.product_id.taxes_id:
                    self.tax_id = self.product_id.taxes_id[0]
                else:
                    self.tax_id = False
        else:
            tax_acc = self.env["config.expense"].search([], limit=1)
            if tax_acc:
                self.tax_account_id = tax_acc.tax_account_id.id
            if self.product_id:
                if self.product_id.supplier_taxes_id:
                    self.tax_id = self.product_id.supplier_taxes_id[0]
                else:
                    self.tax_id = False


    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.debit_account_id = self.product_id.property_account_expense_id.id if self.product_id.property_account_expense_id else self.product_id.categ_id.property_account_expense_categ_id.id
            if self.product_id.supplier_taxes_id:
                self.tax_id = self.product_id.supplier_taxes_id[0]
            else:
                self.tax_id = False

    @api.depends('tax_id', 'amount')
    def _compute_tax_amount(self):
        for record in self:
            if record.tax_id and record.amount:
                if record.tax_id.amount_type == 'percent' and record.tax_id.amount:
                    record.tax_amount = round(record.tax_id.amount * record.amount / 100, 2)
                elif record.tax_id.amount_type == 'fix' and record.tax_id.amount:
                    record.tax_amount = round(record.tax_id.amount, 2)
                else:
                    raise UserError(
                        'Not implemented procedure for this type of tax. Only Percent and Fix are taken into account.')
            else:
                record.tax_amount = 0

    @api.depends("amount", "tax_amount", "has_iva")
    def _compute_total(self):
        for record in self:
            record.total = record.amount + record.tax_amount if record.has_iva else record.amount
            record.write({'total_amount': record.total})

    def _init_tax_account_id(self):
        account_set = self.env["config.expense"].search([], limit=1)
        if account_set:
            self.tax_account_id = account_set.tax_account_id
        else:
            self.tax_account_id = False


    name = fields.Char('Description', readonly=True, states={'draft': [('readonly', False)]})
    code = fields.Char()
    expense_date = fields.Datetime('Expense date', default=lambda self: fields.Datetime.now(), readonly=True,
                                   states={'draft': [('readonly', False)]})
    product_id = fields.Many2one('product.template', 'Product', readonly=True, states={'draft': [('readonly', False)]},
                                 tracking=True)
    amount = fields.Float('Amount', readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    debit_account_id = fields.Many2one('account.account', 'Debit account', readonly=True,
                                       states={'draft': [('readonly', False)]}, tracking=True)
    payment_method_id = fields.Many2one('account.journal', 'Payment method', tracking=True,
                                        help='Payment method or Account journal, usually with cash type.',
                                        readonly=True,
                                        states={'draft': [('readonly', False)]})
    has_iva = fields.Boolean('IVA?', readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    tax_account_id = fields.Many2one('account.account', 'Tax account',
                                     default= "_init_tax_account_id",
                                     readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    tax_id = fields.Many2one('account.tax', 'Tax', readonly=True, states={'draft': [('readonly', False)]},
                             tracking=True)
    tax_amount = fields.Float('Tax Amount', compute='_compute_tax_amount', tracking=True)
    confirm_move_id = fields.Many2one('account.move', 'Confirm move',
                                      help='Move generated when pressing confirm button',
                                      readonly=True, states={'draft': [('readonly', False)]})
    cancel_move_id = fields.Many2one('account.move', 'Cancel move', help='Move generated when pressing cancel button')
    notes = fields.Html(states={'cancelled': [('readonly', True)]}, tracking=True)
    state = fields.Selection([('draft', 'Created'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], 'State',
                             default='draft', tracking=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company,
                                 tracking=True)
    refund_expense = fields.Boolean(string="Refund expense?", default=False)
    employee_id = fields.Many2one('hr.employee', 'Employee')
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
            vals['code'] = self.env['ir.sequence'].next_by_code('account.expense.seq')
        res = super(AccountExpense, self).create(vals)
        return res

    def set_confirmed(self):
        for record in self:
            record.sudo().generate_account_move_confirm_iva() if record.has_iva else record.sudo().generate_account_move_confirm()
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
        return super(AccountExpense, self).unlink()

    def generate_account_move_confirm_iva(self):
        move_data = {
            "journal_id": self.payment_method_id.id,
            "ref": self.name,
            "date": self.expense_date,
            "state": "draft",
        }
        total_debit = 0
        lines_w_iva = []
        lines_w_iva.append(
            (0, 0, {
                "partner_id": False,
                "account_id": self.debit_account_id.id,
                "name": self.name,
                "debit": abs(self.amount),
                "credit": 0.00, },)
        )
        total_debit += self.amount
        lines_w_iva.append(
            (0, 0, {
                "partner_id": False,
                "account_id": self.tax_account_id.id,
                "name": self.name,
                "debit": abs(self.tax_amount),
                "credit": 0.00, },))
        total_debit = abs(total_debit + self.tax_amount)

        lines_w_iva.append(
            (0, 0, {
                "account_id": self.payment_method_id.payment_credit_account_id.id,
                "name": self.name,
                "debit": 0.00,
                "credit": total_debit,
            },))
        move_data.update({"line_ids": lines_w_iva})
        move = self.env["account.move"].create(move_data)
        move.write({"state": "posted"})
        self.write({"confirm_move_id": move.id})
        return True

    def generate_account_move_confirm(self):
        move_data = {
            "journal_id": self.payment_method_id.id,
            "ref": self.name,
            "date": self.expense_date,
            "state": "draft",
        }
        total_debit = 0
        lines = []
        lines.append(
            (
                0,
                0,
                {
                    "partner_id": False,
                    "account_id": self.debit_account_id.id,
                    "name": self.name,
                    "debit": abs(self.amount),
                    "credit": 0.00,
                },
            )
        )
        total_debit = self.amount

        lines.append(
            (0, 0, {
                "account_id": self.payment_method_id.payment_credit_account_id.id,
                "name": self.name,
                "debit": 0.00,
                "credit": total_debit,
            },
             )
        )

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
            'amount': self.total * -1,
            'unit_amount': 1,
            'product_id': self.env["product.product"].search([('product_tmpl_id', '=', self.product_id.id)],
                                                             limit=1).id,
            'move_id': self.confirm_move_id.line_ids[0].id
        }
        move_id = self.env["account.analytic.line"].create(val)
        self.write({'account_analytic_line_id': move_id.id})
