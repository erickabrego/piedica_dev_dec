from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ConfigExpense(models.Model):
    _name = 'config.expense'

    tax_account_id = fields.Many2one('account.account', 'Tax account',company_dependent=True,
                                     config_parameter='ateneolab_expense.tax_account_id')
    tax_account_refund_id = fields.Many2one('account.account', 'Tax account refund', company_dependent=True,
                                     config_parameter='ateneolab_expense.tax_account_refund_id')

    @api.model
    def create(self, vals_list):
        account_config = self.search([])
        if account_config:
            raise UserError(_("Ya existe una configuración de cuentas, edite la existente"))
        return super(ConfigExpense, self).create(vals_list)
