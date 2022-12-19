from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_tag_manager_key = fields.Char('Google Tag Manager Key', related='website_id.google_tag_manager_key', readonly=False)

    @api.depends('website_id')
    def has_google_tag_manager(self):
        self.has_google_tag_manager = bool(self.google_tag_manager_key)

    def inverse_has_google_tag_manager(self):
        if not self.has_google_tag_manager:
            self.google_tag_manager_key = False

    has_google_tag_manager = fields.Boolean("Google Tag Manager", compute=has_google_tag_manager, inverse=inverse_has_google_tag_manager)
