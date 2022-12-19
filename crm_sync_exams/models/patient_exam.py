import datetime
import re

from odoo import models, fields, api

class PatientExam(models.Model):
    _name = 'patient.exam'
    _description = 'Estudio del paciente'
    _order = 'date asc'

    patient_id = fields.Many2one('res.partner', string='Paciente', help='Identificador del paciente en Odoo.')
    exam_crm_id = fields.Integer('ID estudio CRM', help='Es el identificador único del estudio de un paciente en CRM.')
    branch_id = fields.Many2one('res.partner', string='Sucursal', help='Identificador de la sucursal en la que se realizaron los estudios. Este campo debe coincidir ya con las sucursales existentes en Odoo.')
    date_crm = fields.Datetime('Fecha de creación en CRM', help='Fecha y hora de creación del estudio, proveniente de CRM.')
    file = fields.Char('Archivo', help='Nombre del archivo zip del estudio que se encuentra registrado en CRM.')

    exam_status_id = fields.Many2one('exam.status', string='Estatus del estudio médico', help='Identificador de los estatus del flujo del proceso de las solicitudes de estudios (No solicitado, Solicitado, Generado).')
    date = fields.Datetime('Fecha de creación', help='Fecha y hora en la que se creó el registro en Odoo.')
    drive_file = fields.Char('Archivo en Drive', help='Nombre del archivo del estudio pdf que se encuentra en drive.')
    drive_folder = fields.Char('Carpeta en Drive', help='Nombre de la ruta de drive donde se encuentra el estudio PDF.')
    exam_status_history = fields.One2many('exam.status.history', 'exam_id', string='Historial de estatus')


    def create_exam(self, args):
        args_status = self.validate_create_data(args)

        if args_status['status'] == 'error':
            return args_status

        data = args_status['content']
        data.update({'date': datetime.datetime.now()})
        patient_exam = self.with_context(lang='es_MX').create(data)

        if patient_exam.drive_file:
            exam_status = self.env['exam.status'].search([('code', '=', 'generado')])
            patient_exam.send_exams_ready_email()
        else:
            exam_status = self.env['exam.status'].search([('code', '=', 'no_solicitado')])
            patient_exam.send_exams_available_email()

        patient_exam.write({'exam_status_id': exam_status.id})
        patient_exam.create_exam_status()

        return {
            'status': 'success',
            'content': {
                'patient_exam': patient_exam.id
            }
        }


    def to_requested(self):
        self.ensure_one()
        exam_status = self.env['exam.status'].search([('code', '=', 'solicitado')])
        self.write({'exam_status_id': exam_status.id})
        self.create_exam_status()

        activity = self.env['mail.activity'].create({
            'activity_type_id': 4, # Por hacer
            'summary': 'Subir estudios del paciente de la fecha ' + self.date_crm.strftime('%d/%m/%Y'),
            'date_deadline': datetime.date.today(),
            'user_id': self.branch_id.exams_manager.id,
            'res_model_id': 79, # Contacto
            'res_id': self.patient_id.id
        })


    def to_generated(self, args):
        self.ensure_one()
        args_status = self.validate_update_data(args)

        if args_status['status'] == 'error':
            return args_status

        data = args_status['content']
        exam_status = self.env['exam.status'].search([('code', '=', 'generado')])

        self.write({
            'exam_status_id': exam_status.id,
            'drive_file': data['drive_file'],
            'drive_folder': data['drive_folder']
        })

        self.create_exam_status()
        self.send_exams_ready_email()

        return {
            'status': 'success'
        }


    def create_exam_status(self):
        self.ensure_one()

        self.write({
            'exam_status_history': [(0, 0, {
                'exam_id': self.id,
                'exam_status_id': self.exam_status_id.id,
                'date': datetime.datetime.now()
            })]
        })


    def send_exams_available_email(self):
        self.ensure_one()

        template = self.env['mail.template'].search([('name', '=', 'PD_solicita_estudios')])
        template.send_mail(self.id, force_send=True)


    def send_exams_requested_email(self):
        self.ensure_one()

        template = self.env['mail.template'].search([('name', '=', 'PD_estudios_solicitados')])
        template.send_mail(self.id, force_send=True)


    def send_exams_ready_email(self):
        self.ensure_one()

        template = self.env['mail.template'].search([('name', '=', 'PD_estudios_listos')])
        template.send_mail(self.id, force_send=True)


    def validate_create_data(self, args):
        patient_id = args.get('patient', None) # Paciente
        exam_crm_id = args.get('exam_crm', None) # ID estudio CRM
        branch_id = args.get('branch', None) # Sucursal
        date_crm = args.get('date_crm', None) # Fecha de creación en CRM
        file = args.get('file', None) # Nombre del archivo zip

        drive_file = args.get('drive_file', None) # Nombre del archivo pdf
        drive_folder = args.get('drive_folder', None) # Nombre de la carpeta del archivo pdf

        missing_args = []

        # Comprueba que se hayan suplido todos los argumentos
        if not patient_id:
            missing_args.append('patient')
        else:
            if not isinstance(patient_id, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro patient debe ser un valor numérico. Valor introducido: %s' % str(patient_id)
                }

            patient_record = self.env['res.partner'].search([('id', '=', patient_id)])

            if not patient_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró el paciente con el id %s' % patient_id
                }


        if not exam_crm_id:
            missing_args.append('exam_crm')
        else:
            if not isinstance(exam_crm_id, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro exam_crm debe ser un valor numérico. Valor introducido: %s' % str(exam_crm_id)
                }

            if self.search_count([('exam_crm_id', '=', exam_crm_id)]) > 0:
                return {
                    'status': 'error',
                    'message': 'Ya existe un estudio con el id de crm %d' % exam_crm_id
                }


        if not branch_id:
            missing_args.append('branch')
        else:
            if not isinstance(branch_id, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro branch debe ser un valor numérico. Valor introducido: %s' % str(branch_id)
                }

            branch_record = self.env['res.partner'].search([('id', '=', branch_id)])

            if not branch_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró la sucursal con el id %s' % branch_id
                }


        if not date_crm:
            missing_args.append('date_crm')
        else:
            if not isinstance(date_crm, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro date_crm debe ser un string. Valor introducido: %s' % str(date_crm)
                }

            if not re.search('^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$', date_crm):
                return {
                    'status': 'error',
                    'message': 'El formato de fecha de date_crm debe ser YYYY-MM-DD HH:MM:SS. Valor introducido: %s' % str(date_crm)
                }

            try:
                datetime.datetime.strptime(date_crm, '%Y-%m-%d %H:%M:%S')
            except:
                return {
                    'status': 'error',
                    'message': 'El valor de date_crm no es una fecha válida'
                }


        if not file:
            missing_args.append('file')
        else:
            if not isinstance(file, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro file debe ser un string. Valor introducido: %s' % str(file)
                }


        if missing_args:
            return {
                'status': 'error',
                'message': 'Faltan los siguientes argumentos: %s' % ', '.join(missing_args)
            }

        data = {
            'patient_id': patient_id,
            'exam_crm_id': exam_crm_id,
            'branch_id': branch_id,
            'date_crm': date_crm,
            'file': file
        }


        # Parametros opcionales
        if drive_file:
            if not isinstance(drive_file, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro drive_file debe ser un string. Valor introducido: %s' % str(drive_file)
                }
            else:
                data.update({'drive_file': drive_file})


        if drive_folder:
            if not isinstance(drive_folder, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro drive_folder debe ser un string. Valor introducido: %s' % str(drive_folder)
                }
            else:
                data.update({'drive_folder': drive_folder})


        return {
            'status': 'success',
            'content': data
        }


    def validate_update_data(self, args):
        drive_file = args.get('drive_file', None) # Nombre del archivo pdf
        drive_folder = args.get('drive_folder', None) # Nombre de la carpeta del archivo pdf

        missing_args = []

        # Comprueba que se hayan suplido todos los argumentos
        if not drive_file:
            missing_args.append('drive_file')
        else:
            if not isinstance(drive_file, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro drive_file debe ser un string. Valor introducido: %s' % str(drive_file)
                }


        if not drive_folder:
            missing_args.append('drive_folder')
        else:
            if not isinstance(drive_folder, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro drive_folder debe ser un string. Valor introducido: %s' % str(drive_folder)
                }


        if missing_args:
            return {
                'status': 'error',
                'message': 'Faltan los siguientes argumentos: %s' % ', '.join(missing_args)
            }


        return {
            'status': 'success',
            'content': {
                'drive_file': drive_file,
                'drive_folder': drive_folder
            }
        }
