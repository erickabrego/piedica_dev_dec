from odoo import http, _
from odoo.http import request


class CustomerRegistration(http.Controller):

    @http.route('/code', type='http', auth='public', website=True, csrf=False)
    def code(self, **kw):
        request.env['ir.config_parameter'].sudo().set_param('allene_zoom_integration.code', kw.get("code"))
        return request.render("allene_zoom_integration.code_generation")
