import datetime
import re
import logging

from odoo import http
from odoo.addons.website_calendar.controllers.main import WebsiteCalendar
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteCalendarController(WebsiteCalendar):

    @http.route(['/calendar/<model("calendar.appointment.type"):appointment_type>/submit'], type='http', auth="public", website=True, methods=["POST"])
    def calendar_appointment_submit(self, appointment_type, datetime_str, employee_id, name, phone, email, country_id=False, **kwargs):
        # En caso de que el usuario no haya iniciado sesión, verifica si el
        # correo ingresado ya está registrado
        if request.env.user._is_public():
            user_domain = ['|', ('login', '=like', email), ('email', '=like', email)]

            if request.env['res.users'].sudo().search(user_domain):
                return_url = request.httprequest.headers.get('Referer')

                return request.render('appointment_leads.p_email_error', {
                    'return_url': return_url,
                    'email': email
                })


        res = super(WebsiteCalendarController, self).calendar_appointment_submit(appointment_type, datetime_str, employee_id, name, phone, email, country_id, **kwargs)

        # Crea una oportunidad a partir de la cita
        if appointment_type.p_lead_create:
            if not '/appointment?failed' in res.location:
                partner = request.env['res.partner'].sudo().search([('email', '=like', email)], limit=1)
                stage_name = 'Agenda cita'
                stage = request.env['crm.stage'].sudo().search([('name', '=', stage_name)])

                if partner and stage:
                    opportunity = request.env['crm.lead'].sudo().create({
                        'name': partner.name + ' oportunidad',
                        'partner_id': partner.id,
                        'email_from': email,
                        'phone': phone,
                        'stage_id': stage.id,
                        'user_id': None,
                        'expected_revenue': 0,
                        'probability': 0.0
                    })

                    access_token_match = re.search('/calendar/view/(.*)\?message=new', res.location)

                    if access_token_match:
                        access_token = access_token_match.group(1)
                        event = request.env['calendar.event'].sudo().search([('access_token', '=', access_token)])

                        if event:
                            event.write({
                                'opportunity_id': opportunity.id
                            })
                else:
                    if not partner:
                        _logger.error('No se ha encontrado el contacto con el email %s. No se ha podido crear la oportunidad.' % email)

                    if not stage:
                        _logger.error('No se ha encontrado la etapa %s. No se ha podido crear la oportunidad.' % stage_name)

        return res


    @http.route(['/calendar/view/<string:access_token>'], type='http', auth="public", website=True)
    def calendar_appointment_view(self, access_token, edit=False, message=False, **kwargs):
        res = super(WebsiteCalendarController, self).calendar_appointment_view(access_token, edit, message, **kwargs)

        event = request.env['calendar.event'].sudo().search([('access_token', '=', access_token)], limit=1)

        # Crea un usuario para quien agendó la cita en caso de que sea su primera cita
        # (osea que aún no tenga una cuenta)
        if event:
            if event.partner_ids:
                partner = event.partner_ids.filtered(lambda partner: partner.id != event.partner_id.id)[0]
                user_domain = ['|', ('login', '=like', partner.email), ('email', '=like', partner.email)]

                if not request.env['res.users'].sudo().search(user_domain):
                    portal_wizard = request.env['portal.wizard'].sudo().create({
                        'user_ids': [(0, 0, {
                            'partner_id': partner.id,
                            'email': partner.email,
                            'in_portal': True
                        })]
                    })

                    portal_wizard.action_apply()
        return res

    @http.route(['/calendar/<model("calendar.appointment.type"):appointment_type>/appointment'], type='http', auth="public", website=True, sitemap=True)
    def calendar_appointment(self, appointment_type=None, employee_id=None, timezone=None, failed=False, **kwargs):
        res = super(WebsiteCalendarController, self).calendar_appointment(appointment_type, employee_id, timezone, failed, **kwargs)
        x_studio_servicios_1 = dict(request.env['calendar.event'].sudo()._fields['x_studio_servicios_1'].selection)
        res.qcontext.update({"servicios": x_studio_servicios_1})
        return res
