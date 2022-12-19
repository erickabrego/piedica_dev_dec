from odoo.exceptions import UserError
from odoo import fields, models, api, _
from datetime import date, datetime


class Company(models.Model):
    _inherit = "res.company"

    @api.onchange("company_type_commission")
    def onchange_company_commission_type(self):
        if self.company_type_commission:
            if self.company_type_commission == "independent":
                self.commission_percent = 0
            if self.company_type_commission == "matrix":
                self._evaluate_company_type_commission()

    def _evaluate_company_type_commission(self):
        companys = self.search([('company_type_commission', '=', 'matrix')])
        if companys:
            raise UserError(_("Ya existe una Sucursal de tipo matriz, solo puede existir una."))

    company_type_commission = fields.Selection(
        [('matrix', 'Matrix'), ('commercial', 'Commercial'), ('independent', 'Independent')], string="Company type",
        default="independent")
    commission_percent = fields.Integer(string="Percent commissions")


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super(AccountMove, self).action_post()
        if self.move_type == "out_invoice" and self.company_id.company_type_commission == "commercial" and self.company_id.commission_percent > 0:
            self._generate_invoice_commission()
        return res

    def _generate_invoice_commission(self):
        company_matrix = self.env["res.company"].search([('company_type_commission', '=', 'matrix')])
        if company_matrix:
            self.sudo().env['account.move'].with_context(default_move_type='out_invoice').create(
                self._prepare_customer_invoice(company_matrix))

    def _prepare_customer_invoice(self, company_matrix):
        vals = {}
        invoice_lines = self._prepare_customer_invoice_line(company_matrix)

        journal = self.sudo().env["account.journal"].search(
            [('company_id', '=', company_matrix.id), ('type', '=', 'sale')], limit=1)

        vals.update({
            'partner_id': self.company_id.partner_id.id,
            'company_id': company_matrix.id,
            'journal_id': journal.id,
            'currency_id': company_matrix.currency_id.id,
            'move_type': 'out_invoice',
            'ref': self.name,
            'invoice_date': self.invoice_date,
            'invoice_date_due': self.invoice_date_due,
            'invoice_line_ids': [i for i in invoice_lines if not i[2].get('exclude_from_invoice_tab', False)],
            'line_ids': invoice_lines,
            'state': 'draft',
        })
        return vals

    def _prepare_customer_invoice_line(self, company_matrix):
        res = []
        product_template = self.sudo().env["product.template"].search(
            [('is_commission', '=', True)], limit=1)
        if not product_template:
            raise UserError(_("Debe configurar un producto para las comisiones."))

        product_product = self.sudo().env["product.product"].search(
            [('product_tmpl_id', '=', product_template.id)])

        account = product_template.property_account_income_id or product_template.categ_id.property_account_income_categ_id
        account_credit = self.sudo().env["account.account"].search(
            [('company_id', '=', company_matrix.id), ('code', '=', account.code)])

        account = self.company_id.partner_id.property_account_receivable_id
        account_debit = self.sudo().env["account.account"].search(
            [('company_id', '=', company_matrix.id), ('code', '=', account.code)])

        amount = self.amount_total * self.company_id.commission_percent / 100
        if self.currency_id.id != company_matrix.currency_id.id:
            amount = round(
                self.currency_id._convert(amount, company_matrix.currency_id, self.env.company,
                                          date.today()), 2)
        res.append((0, 0, {
            'product_id': product_product.id,
            'product_uom_id': product_product.uom_id.id,
            'quantity': 1,
            'price_unit': amount,
            'account_id': account_credit.id,
            'credit': amount,
            'name': product_template.name or "",
            'recompute_tax_line': True,
            'exclude_from_invoice_tab': False,
        }))
        res.append((0, 0, {
            'product_id': product_product.id,
            'product_uom_id': product_product.uom_id.id,
            'quantity': 1,
            'price_unit': amount,
            'account_id': account_debit.id,
            'debit': amount,
            'name': product_template.name or "",
            'recompute_tax_line': False,
            'exclude_from_invoice_tab': True,
        }))

        return res


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_commission = fields.Boolean(string="Commission")
