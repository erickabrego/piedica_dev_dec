import datetime

from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class CustomerPortalController(CustomerPortal):

    def __init__(self):
        super(CustomerPortalController, self).__init__()

        type(self).OPTIONAL_BILLING_FIELDS.extend([
            'p_adult_kid', 'p_birth_date', 'p_age', 'p_occupation', 'p_physical_activity',
            'p_physical_activity_true', 'p_hear_about_us', 'p_hear_about_us_other',
            'p_height', 'p_weight', 'p_shoe_size', 'main_complaints', 'other_complaints',
            'p_contact_you'
        ])


    @http.route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        data = post

        if post and request.httprequest.method == 'POST':
            data = self.update_values(post)

        res = super(CustomerPortalController, self).account(redirect=redirect, **data)

        # Items para los select de "¿Cómo se enteró de nosotros?" y "Principales molestias"
        hear_media = dict(request.env['res.partner'].sudo()._fields['p_hear_about_us'].selection)
        complaints = request.env['patient.complaint'].sudo().search([])

        res.qcontext.update({
            'hear_media': hear_media,
            'complaints': complaints
        })

        # Se necesita que la variable "p_physical_activity" siempre exista en el
        # contexto del template, para poder hacer las comprobaciones de cuál de
        # los dos radio buttons de ese campo debería estar en check
        if not 'p_physical_activity' in res.qcontext:
            res.qcontext.update({'p_physical_activity': None})

        return res


    # Ya que los datos provenientes del formulario no vienen de una manera
    # ideal para algunos campos (ej: los radio buttons vienen en string, cuando
    # debería ser en booleano; los checkbox vienen en tuplas, cuando debería ser
    # en una lista), este método se utiliza para adecuar esos datos
    def update_values(self, data):
        new_data = data

        p_physical_activity = data.get('p_physical_activity', None)

        if p_physical_activity:
            if p_physical_activity == 'True':
                p_physical_activity = True
            elif p_physical_activity == 'False':
                p_physical_activity = False

            new_data['p_physical_activity'] = p_physical_activity


        main_complaints_form = request.httprequest.form.getlist('main_complaints')
        main_complaints_ok = True

        if main_complaints_form:
            main_complaints = []

            for complaint_id in main_complaints_form:
                try:
                    complaint_id = int(complaint_id)
                except:
                    main_complaints_ok = False
                    break

                # Adicionalmente se comprueba que los id's pasados sí existan
                complaint_record = request.env['patient.complaint'].sudo().search([('id', '=', complaint_id)])

                if not complaint_record:
                    main_complaints_ok = False
                    break

                main_complaints.append((4, complaint_id))

            new_data['main_complaints'] = main_complaints if main_complaints_ok else 'error'


        p_contact_you = data.get('p_contact_you', None)

        if p_contact_you:
            if p_contact_you == 'True':
                p_contact_you = True
            elif p_contact_you == 'False':
                p_contact_you = False

            new_data['p_contact_you'] = p_contact_you

        return new_data


    def details_form_validate(self, data):
        errors, error_messages = super(CustomerPortalController, self).details_form_validate(data)

        p_adult_kid = data.get('p_adult_kid')

        if p_adult_kid:
            if p_adult_kid != 'adulto' and p_adult_kid != 'nino':
                errors.update({'p_adult_kid': 'error'})
                error_messages.append('Valor inesperado en ¿Es un adulto o un niño?')


        p_birth_date = data.get('p_birth_date')

        if p_birth_date:
            try:
                datetime.datetime.strptime(p_birth_date, '%Y-%m-%d')
            except:
                errors.update({'p_birth_date': 'error'})
                error_messages.append('La fecha de nacimiento no es una fecha válida')


        p_age = data.get('p_age')

        if p_age:
            try:
                p_age = int(p_age)
            except:
                errors.update({'p_age': 'error'})
                error_messages.append('La edad debe ser un valor numérico')


        p_physical_activity = data.get('p_physical_activity', None)

        if p_physical_activity:
            if p_physical_activity != True and p_physical_activity != False:
                errors.update({'p_physical_activity': 'error'})
                error_messages.append('Valor inesperado en ¿Realiza usted alguna actividad física?')

            if p_physical_activity == True:
                if not data.get('p_physical_activity_true'):
                    errors.update({'p_physical_activity_true': 'error'})
                    error_messages.append('Ingresa la actividad física que realizas')


        p_hear_about_us = data.get('p_hear_about_us', None)

        if p_hear_about_us:
            media_keys = dict(request.env['res.partner'].sudo()._fields['p_hear_about_us'].selection).keys()

            if not p_hear_about_us in media_keys:
                errors.update({'p_hear_about_us': 'error'})
                error_messages.append('Valor inesperado en ¿Cómo se enteró de nosotros?')

            if p_hear_about_us == 'otro':
                if not data.get('p_hear_about_us_other'):
                    errors.update({'p_hear_about_us_other': 'error'})
                    error_messages.append('Ingresa el medio por el cual te enteraste de nosotros')


        p_height = data.get('p_height', None)

        if p_height:
            try:
                p_height = float(p_height)
            except:
                errors.update({'p_height': 'error'})
                error_messages.append('La altura debe ser un valor numérico')


        p_weight = data.get('p_weight', None)

        if p_weight:
            try:
                p_weight = float(p_weight)
            except:
                errors.update({'p_weight': 'error'})
                error_messages.append('El peso debe ser un valor numérico')


        main_complaints = data.get('main_complaints', None)

        if main_complaints == 'error':
            errors.update({'main_complaints': 'error'})
            error_messages.append('Valor inesperado en Principales molestias')


        p_contact_you = data.get('p_contact_you', None)

        if p_contact_you:
            if p_contact_you != True and p_contact_you != False:
                errors.update({'p_contact_you': 'error'})
                error_messages.append('Valor inesperado en ¿Desea que nos comuniquemos con usted?')


        return errors, error_messages
