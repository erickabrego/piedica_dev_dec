import datetime

from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
from dateutil.relativedelta import relativedelta


class CustomerPortalController(CustomerPortal):

    def __init__(self):
        super(CustomerPortalController, self).__init__()

        type(self).OPTIONAL_BILLING_FIELDS.extend(['x_studio_cmo_nos_contacta','x_studio_medio','x_studio_medico',
            'x_studio_nombre_del_paciente_que_lo_recomienda','x_studio_medio_otro','x_studio_gnero',
            'x_studio_cumpleaos', 'p_age', 'p_occupation', 'p_physical_activity',
            'p_physical_activity_true', 'x_studio_altura_cm', 'x_studio_peso_kgs', 'x_studio_talla', 'main_complaints',
            'other_complaints', 'p_contact_you'
        ])


    @http.route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        data = post

        if post and request.httprequest.method == 'POST':
            data = self.update_values(post)

        res = super(CustomerPortalController, self).account(redirect=redirect, **data)

        # Items para los select de "¿Cómo se enteró de nosotros?" y "Principales molestias"
        genders = dict(request.env['res.partner'].sudo()._fields['x_studio_gnero'].selection)
        complaints = request.env['patient.complaint'].sudo().search([])
        how_contact_us = dict(request.env['res.partner'].sudo()._fields['x_studio_cmo_nos_contacta'].selection)
        contact_internet = dict(request.env['res.partner'].sudo()._fields['x_studio_medio'].selection)
        medics = request.env['res.partner'].sudo().search([("x_studio_es_mdico_especialista","=",True)])
        patients = request.env['res.partner'].sudo().search([("x_studio_es_paciente", "=", True)])

        res.qcontext.update({
            'genders': genders,
            'complaints': complaints,
            'how_contact_us': how_contact_us,
            'contact_internet': contact_internet,
            'medics': medics,
            'patients': patients
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

        how_contact_us = data.get('x_studio_cmo_nos_contacta', None)
        if how_contact_us:
            if how_contact_us == 'Internet':
                new_data['x_studio_medico'] = False
                new_data['x_studio_nombre_del_paciente_que_lo_recomienda'] = False
                new_data['x_studio_medio_otro'] = False
            elif how_contact_us == 'Médico / Especialista':
                new_data['x_studio_medio'] = False
                new_data['x_studio_nombre_del_paciente_que_lo_recomienda'] = False
                new_data['x_studio_medio_otro'] = False
            elif how_contact_us == 'Recomendado paciente':
                new_data['x_studio_medio'] = False
                new_data['x_studio_medico'] = False
                new_data['x_studio_medio_otro'] = False
            else:
                new_data['x_studio_medio'] = False
                new_data['x_studio_medico'] = False
                new_data['x_studio_nombre_del_paciente_que_lo_recomienda'] = False

        x_studio_cumpleaos = data.get('x_studio_cumpleaos', None)
        if x_studio_cumpleaos:
            age = relativedelta(datetime.date.today(), datetime.datetime.strptime(x_studio_cumpleaos,'%Y-%m-%d'))
            new_data['p_age'] = age.years


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

        p_birth_date = data.get('x_studio_cumpleaos')

        if p_birth_date:
            try:
                datetime.datetime.strptime(p_birth_date, '%Y-%m-%d')
            except:
                errors.update({'x_studio_cumpleaos': 'error'})
                error_messages.append('La fecha de nacimiento no es una fecha válida')

        p_physical_activity = data.get('p_physical_activity', None)

        if p_physical_activity:
            if p_physical_activity != True and p_physical_activity != False:
                errors.update({'p_physical_activity': 'error'})
                error_messages.append('Valor inesperado en ¿Realiza usted alguna actividad física?')

            if p_physical_activity == True:
                if not data.get('p_physical_activity_true'):
                    errors.update({'p_physical_activity_true': 'error'})
                    error_messages.append('Ingresa la actividad física que realizas')

        p_height = data.get('x_studio_altura_cm', None)

        if p_height:
            try:
                p_height = int(p_height)
            except:
                errors.update({'x_studio_altura_cm': 'error'})
                error_messages.append('La altura debe ser un valor numérico')


        p_weight = data.get('x_studio_peso_kgs', None)

        if p_weight:
            try:
                p_weight = int(p_weight)
            except:
                errors.update({'x_studio_peso_kgs': 'error'})
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
