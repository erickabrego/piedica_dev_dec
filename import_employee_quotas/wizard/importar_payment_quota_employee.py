# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
import xlrd
from xlrd import open_workbook
import base64
import os
from odoo.modules import module
from odoo.exceptions import UserError, ValidationError
import datetime

class ImportPaymentQuotaEmployee(models.TransientModel):
    _name = 'import.payment.quota.employee'

    excel = fields.Binary('Excel file (recommended format: xlsx) to import')

    def importar(self):
        obj_payment_quota = self.env['payment.quota.employee'].search([('id', '=', self.env.context.get('active_id', None))])
        obj_payment_quota_line = self.env['payment.quota.employee.line']
        path = os.path.join(module.get_module_path('import_employee_quotas'), 'tmp', 'payment_quota_employee.xlsx')
        fileobj = open(path, "wb")
        if self.excel != False:
            fileobj.write(base64.b64decode(self.excel))
            fileobj.flush()
            fileobj.close()
            try:
                wb = open_workbook(path)
            except:
                raise UserError(_('Select an excel file!'))

            pestanna = wb.sheet_by_index(0)
            numero_filas = pestanna.nrows

            process_date = pestanna.cell_value(rowx=6, colx=13)
            process_date = datetime.datetime(*xlrd.xldate_as_tuple(process_date, 0))

            obj_payment_quota.write({
                'process_period': pestanna.cell_value(rowx=7, colx=7).split(':')[1],
                'record_patronal': pestanna.cell_value(rowx=9, colx=3),
                'process_date': process_date,
                'name_reason_social': pestanna.cell_value(rowx=11, colx=3),
                'activity': pestanna.cell_value(rowx=12, colx=3),
           })

            for nro_fila in range(22, numero_filas):
               lic =  pestanna.cell_value(rowx=nro_fila, colx=0)
               if lic == '' or lic=='Baja' or lic=='Alta' or lic=='M/S':
                   pass
               elif  lic=='Total de Días cotizados para el calculo de trabajadores promedio expuestos al riesgo':
                   break
               else:
                   fila_2 = nro_fila+2
                   valores = {
                       'key_code': pestanna.cell_value(rowx=nro_fila, colx=0),
                       'days': pestanna.cell_value(rowx=fila_2, colx=3),
                       'sdi': pestanna.cell_value(rowx=fila_2, colx=4),
                       'lic': pestanna.cell_value(rowx=nro_fila, colx=5),
                       'patronal': pestanna.cell_value(rowx=fila_2, colx=19),
                       'worker': pestanna.cell_value(rowx=fila_2, colx=20),
                       'subtotal': pestanna.cell_value(rowx=fila_2, colx=21),
                       'sucursal': pestanna.cell_value(rowx=nro_fila, colx=22),
                       'payment_quota_id': obj_payment_quota.id
                   }
                   fecha = pestanna.cell_value(rowx=fila_2, colx=2)
                   if fecha != "":
                       fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y")
                       valores['date'] = fecha

                   obj_payment_quota_line.create(valores)



