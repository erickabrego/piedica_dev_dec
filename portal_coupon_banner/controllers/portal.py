from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()

        partner = request.env.user.partner_id
        values['patient_coupon'] = partner.sudo().get_available_coupon().code if partner.sudo().get_available_coupon() else None

        return values
