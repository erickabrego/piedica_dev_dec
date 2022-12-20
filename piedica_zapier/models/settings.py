from odoo import models, fields, api

class ZapierSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    development_environment = fields.Boolean(string='Ambiente de desarrollo', default=False)
    zapier_key = fields.Char(string='Llave Zapier')
    facebook_salesperson = fields.Many2one('res.users', string='Comercial de Facebook', ondelete='set null')
    web_page_salesperson = fields.Many2one('res.users', string='Comercial de Página web', ondelete='set null')


    def set_values(self):
        res = super(ZapierSettings, self).set_values()

        facebook_salesperson = self.facebook_salesperson and self.facebook_salesperson.id or False
        web_page_salesperson = self.web_page_salesperson and self.web_page_salesperson.id or False

        self.env['ir.config_parameter'].set_param('piedica_zapier.zapier_key', self.zapier_key)
        self.env['ir.config_parameter'].set_param('piedica_zapier.facebook_salesperson', facebook_salesperson)
        self.env['ir.config_parameter'].set_param('piedica_zapier.web_page_salesperson', web_page_salesperson)

        return res


    @api.model
    def get_values(self):
        res = super(ZapierSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()

        zapier_key = ICPSudo.get_param('piedica_zapier.zapier_key')
        facebook_salesperson = int(ICPSudo.get_param('piedica_zapier.facebook_salesperson'))
        web_page_salesperson = int(ICPSudo.get_param('piedica_zapier.web_page_salesperson'))

        res.update(
            zapier_key=zapier_key,
            facebook_salesperson=facebook_salesperson,
            web_page_salesperson=web_page_salesperson
        )

        return res
