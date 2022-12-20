from odoo import http
from odoo.http import request



class QRCodeController(http.Controller):

    @http.route('/mrp_qrcode/scan_qrcode/<qrcode>', type='http', auth='user')
    def scan_qrcode(self, qrcode, **kwargs):
        mrp_order = request.env['mrp.production'].sudo().search([('id', '=', qrcode)])


        if not mrp_order:
            #return {'warning': 'No picking corresponding to barcode %(barcode)s' % {'barcode': barcode}}
            return 'orden no encontrada'

        if mrp_order.state not in ['confirmed', 'progress','done']:
            return 'nada por hacer'

        result = mrp_order.sudo().operations_next_stage()

        return result
