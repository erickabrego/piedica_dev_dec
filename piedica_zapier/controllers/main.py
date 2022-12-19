from odoo import http, fields
from odoo.http import Controller, request, route, Response


class PiedicaController(Controller):
    @route('/leads/save', type='json', auth='none')
    def save_info(self, **kwargs):
        authorization_key = request.env['ir.config_parameter'].sudo().get_param('piedica_zapier.zapier_key')
        request_auth_key = request.httprequest.authorization['username']

        if not authorization_key == request_auth_key:
            return {
                'error': 'No tienes permisos para realizar esta operacion'
            }

        d_name = kwargs.get('name', None)
        d_email = kwargs.get('email', None)
        d_phone = kwargs.get('phone', None)
        d_company = request.env['res.company'].sudo().search([('name', '=', 'CDOM')])
        d_language = request.env['res.lang'].sudo().search([('code', '=', 'es_MX')])
        d_categories = None
        d_message = kwargs.get('message', None)
        d_medium = request.env['utm.medium'].sudo().search([('name', '=', kwargs.get('medium', None))])
        d_source_id = None
        d_campaign_id = None
        d_salesperson_id = None
        d_stage = request.env['crm.stage'].sudo().search([('name', '=', 'New')])


        categories = kwargs.get('categories', None)

        if categories:
            d_categories = []
            categories_list = categories.split(',')

            for category in categories_list:
                category_obj = request.env['crm.tag'].sudo().search([('name', '=', category)])

                if category_obj:
                    d_categories.append((4, category_obj.id, 0))


        if d_medium.name == 'facebook':
            d_salesperson_id = int(request.env['ir.config_parameter'].sudo().get_param('piedica_zapier.facebook_salesperson'))

            campaign = kwargs.get('campaign', None)
            d_campaign = request.env['utm.campaign'].sudo().search([('name', '=', campaign)])

            if not d_campaign and campaign:
                d_campaign = request.env['utm.campaign'].sudo().create({
                    'name': campaign,
                    'user_id': d_salesperson_id
                })

            d_campaign_id = d_campaign.id
            source = kwargs.get('source', None)
            d_source = request.env['utm.source'].sudo().search([('name', '=', source)])

            if not d_source and source:
                d_source = request.env['utm.source'].sudo().create({
                    'name': source
                })

            d_source_id = d_source.id
        else:
            d_salesperson_id = int(request.env['ir.config_parameter'].sudo().get_param('piedica_zapier.web_page_salesperson'))


        data = {
            'name': d_name, # Nombre oportunidad
            'email_from': d_email, # Correo electrónico
            'phone': d_phone, # Teléfono
            'company_id': d_company.id, # Compañía
            'tag_ids': d_categories, # Categoría
            'description': d_message, # Notas internas
            'lang_id': d_language.id, # Idioma
            'campaign_id': d_campaign_id, # Campaña
            'medium_id': d_medium.id, # Medio
            'source_id': d_source_id, # Origen
            'user_id': d_salesperson_id, # Comercial
            'stage_id': d_stage.id # Etapa
        }

        record = request.env['crm.lead'].sudo().create(data)
