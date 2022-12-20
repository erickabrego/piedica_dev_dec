import base64
import requests
from datetime import datetime as dt
from odoo.exceptions import Warning
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    client_id = fields.Char("Client ID")
    client_secret = fields.Char("Client Secret")
    code = fields.Char("Code")
    access_token = fields.Char("Access Token")
    refresh_token = fields.Char("Refresg Token")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['client_id'] = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.client_id')
        res['client_secret'] = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.client_secret')
        res['code'] = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.code')
        res['access_token'] = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.access_token')
        res['refresh_token'] = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.refresh_token')
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('zoom_integration.client_id', self.client_id)
        self.env['ir.config_parameter'].sudo().set_param('zoom_integration.client_secret', self.client_secret)
        self.env['ir.config_parameter'].sudo().set_param('zoom_integration.code', self.code)
        self.env['ir.config_parameter'].sudo().set_param('zoom_integration.access_token', self.access_token)
        self.env['ir.config_parameter'].sudo().set_param('zoom_integration.refresh_token', self.refresh_token)
        super(ResConfigSettings, self).set_values()

    def generate_code(self):
        client_id = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.client_id')
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url = base_url + '/code'
        url = "https://zoom.us/oauth/signin?_rnd=1620971507726&client_id=" + client_id + "&redirect_uri=" + base_url + "&response_type=code"

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    def generate_access_token(self):
        code = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.code')
        client_id = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.client_id')
        client_secret = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.client_secret')
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url = base_url + '/code'
        if code and client_id and client_secret:
            auth = client_id + ":" + client_secret
            Authorization = base64.b64encode(auth.encode("ascii")).decode("ascii")
            headers = {
                "Authorization": Authorization,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": base_url,
                "client_id": client_id,
                "client_secret": client_secret
            }
            res = requests.post("https://zoom.us/oauth/token", headers=headers, data=data)
            if res.json().get("error"):
                raise Warning("Please Generate the Code Again")
            else:
                self.env['ir.config_parameter'].sudo().set_param('zoom_integration.access_token', res.json().get("access_token"))
                self.env['ir.config_parameter'].sudo().set_param('zoom_integration.refresh_token', res.json().get("refresh_token"))
        else:
            raise Warning("Please first set Client ID or Client Secret or Generate the Code")

    def refresh_access_token(self):
        client_id = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.client_id')
        client_secret = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.client_secret')
        refresh_token = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.refresh_token')
        if client_id and client_secret:
            auth = client_id + ":" + client_secret
            Authorization = base64.b64encode(auth.encode("ascii")).decode("ascii")
            headers = {
                "Authorization": Authorization,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret
            }
            res = requests.post("https://zoom.us/oauth/token", headers=headers, data=data)
            print ("\n \n res", res.json())
            if res.json().get("error"):
                raise Warning (res.json().get("reason"))
            else:
                self.env['ir.config_parameter'].sudo().set_param('zoom_integration.access_token', res.json().get("access_token"))
                self.env['ir.config_parameter'].sudo().set_param('zoom_integration.refresh_token', res.json().get("refresh_token"))
