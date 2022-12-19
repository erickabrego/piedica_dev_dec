# -*- coding: utf-8 -*-
import base64
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
import xlsxwriter
import io
import itertools
import pytz

from odoo import api, fields, models


class SaleReportWizard(models.TransientModel):
    _name = 'sale.report.wizard'

    @api.onchange('end_date', 'init_date')
    def onchange_date(self):
        if self.end_date <= self.init_date:
            self.end_date = self.init_date

    init_date = fields.Date('Fecha inicio', default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    end_date = fields.Date('Fecha Fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    company_ids = fields.Many2many('res.company', 'wizard_company_rel', 'wz_id', 'cmpny_id', 'Empresas',
                                   default=lambda self: self.env.companies.ids)
    data_file = fields.Binary('Reporte de ventas')

    def print_sale_report(self):
        sales = self.env["sale.order"].sudo()
        out = io.BytesIO()

        # Obteniendo DATOS del reporte
        local_tz = pytz.timezone(
            self.env.user.sudo().tz or 'GMT')
        if local_tz:
            init_tz1 = datetime.combine(self.init_date, datetime.min.time())
            end_tz1 = datetime.combine(self.end_date, datetime.max.time())
            init_utc = local_tz.localize(init_tz1)
            end_utc = local_tz.localize(end_tz1)
            init_tz = init_utc.astimezone(pytz.utc)
            end_tz = end_utc.astimezone(pytz.utc)
        sales_obj = sales.search([("state", "in", ["sale"]), ('company_id', 'in', self.company_ids.ids),
                                  ('create_date', '>=', init_tz), ('create_date', '<=', end_tz)],
                                 order='create_date asc')
        datos = []

        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(out, {'in_memory': True})
        worksheet = workbook.add_worksheet("Acceso")
        for sl in sales_obj:
            date_tz = sl.create_date
            tz1 = self.env.user.sudo().tz
            if tz1 and date_tz:
                date_utc = pytz.UTC.localize(sl.create_date)
                date_tz = date_utc.astimezone(pytz.timezone(tz1))
            date_tz = datetime.strftime(date_tz, DEFAULT_SERVER_DATETIME_FORMAT) if date_tz else ''
            # Revisar PO asociadas a la venta
            status = ''  # Si se hizo orden de compra 'Pedido'. Si se dio entrada al inventario 'En sucursal'. Si ya se hizo la entrega 'Entregado'.
            po = self.env['purchase.order'].search([('origin', '=', sl.name), ('company_id', 'in', self.company_ids.ids),])
            if len(po) > 0:
                if sl.picking_ids and sl.picking_ids[0].state in ['done']:
                    status = 'Entregado'
                elif po[0].picking_ids and po[0].picking_ids[0].state in ['done']:
                    status = 'En sucursal'
                else:
                    status = 'Pedido'

            studio = sl.x_studio_selection_field_waqzv  # Tipo de pedido en alguna personalización por STudio
            invoice = 'SÍ' if any(invo.l10n_mx_edi_cfdi_uuid != False for invo in sl.invoice_ids) else ''
            envio_line = False
            for sline in sl.order_line:
                if sline.product_id and 'Envío' in sline.product_id.name:
                    envio_line = sline
                    break
            envio = envio_line.price_unit if envio_line else 0.00
            urgente_line = False
            for uline in sl.order_line:
                if uline.filtered(lambda x: x.product_id and 'urgente' in x.product_id.name):
                    urgente_line = uline
                    break
            urgente = urgente_line.price_subtotal if urgente_line else 0.00
            payment_ids = []
            Amove = self.env['account.move']
            Apay = self.env['account.payment']
            p_ids = []
            for inv in sl.invoice_ids:
                p_ids = Amove.search(
                    [('move_type', '=', 'entry'), ('ref', '=', inv.payment_reference), ('payment_id', '!=', False), ('company_id', 'in', [sl.company_id.id])],
                    order='create_date desc').mapped('payment_id')
                payment_ids += Apay.search([('id', 'in', p_ids.ids)], order='date asc')
            invoiced = sum(sl.invoice_ids.mapped('amount_total'))
            paid = sum([p.amount for p in payment_ids])
            # Obtener p1, p2 y p3
            pm1 = []
            pm2 = []
            pm3 = []
            date_list = []
            iter_date = 0
            for paym in payment_ids:
                if iter_date < 3:
                    dt = fields.Date.to_date(datetime.strftime(paym.date, '%Y-%m-%d')) # anteriormente paym.create_date
                    if dt not in date_list:
                        date_list.append(dt)
                        iter_date += 1
                else:
                    continue

            for pm in payment_ids:
                this_pm = fields.Date.to_date(datetime.strftime(pm.date, '%Y-%m-%d'))
                if this_pm == date_list[0]:
                    pm1.append(pm)
                elif len(date_list) > 1 and this_pm == date_list[1]:
                    pm2.append(pm)
                elif len(date_list) > 2 and this_pm == date_list[2]:
                    pm3.append(pm)
            fechap1 = ''
            efectivo1 = 0
            tarjeta1 = 0
            amex1 = 0
            dep_transf1 = 0
            mercadopago1 = 0
            if len(pm1) > 0:
                fechap1 = datetime.strftime(pm1[0].date, DEFAULT_SERVER_DATETIME_FORMAT)
                for pago1 in pm1:
                    if pago1.journal_id.type == 'cash':
                        efectivo1 += pago1.amount
                    elif pago1.journal_id.type == 'bank' and 'Tarjeta' in pago1.journal_id.name:
                        tarjeta1 += pago1.amount
                    elif pago1.journal_id.type == 'bank' and 'AMEX' in pago1.journal_id.name:
                        amex1 += pago1.amount
                    elif pago1.journal_id.type == 'bank' and 'Transferencia' in pago1.journal_id.name:
                        dep_transf1 += pago1.amount
                    elif pago1.journal_id.type == 'bank' and 'Mercado pago' in pago1.journal_id.name:
                        mercadopago1 += pago1.amount
            fechap2 = ''
            efectivo2 = 0
            tarjeta2 = 0
            amex2 = 0
            dep_transf2 = 0
            mercadopago2 = 0
            if len(pm2) > 0:
                fechap2 = datetime.strftime(pm2[0].date, DEFAULT_SERVER_DATETIME_FORMAT)
                for pago2 in pm2:
                    if pago2.journal_id.type == 'cash':
                        efectivo2 += pago2.amount
                    elif pago2.journal_id.type == 'bank' and 'Tarjeta' in pago2.journal_id.name:
                        tarjeta2 += pago2.amount
                    elif pago2.journal_id.type == 'bank' and 'AMEX' in pago2.journal_id.name:
                        amex2 += pago2.amount
                    elif pago2.journal_id.type == 'bank' and 'Transferencia' in pago2.journal_id.name:
                        dep_transf2 += pago2.amount
                    elif pago2.journal_id.type == 'bank' and 'Mercado pago' in pago2.journal_id.name:
                        mercadopago2 += pago2.amount
            fechap3 = ''
            efectivo3 = 0
            tarjeta3 = 0
            amex3 = 0
            dep_transf3 = 0
            mercadopago3 = 0
            if len(pm3) > 0:
                fechap3 = datetime.strftime(pm3[0].date, DEFAULT_SERVER_DATETIME_FORMAT)
                for pago3 in pm3:
                    if pago3.journal_id.type == 'cash':
                        efectivo3 += pago3.amount
                    elif pago3.journal_id.type == 'bank' and 'Tarjeta' in pago3.journal_id.name:
                        tarjeta3 += pago3.amount
                    elif pago3.journal_id.type == 'bank' and 'AMEX' in pago3.journal_id.name:
                        amex3 += pago3.amount
                    elif pago3.journal_id.type == 'bank' and 'Transferencia' in pago3.journal_id.name:
                        dep_transf3 += pago3.amount
                    elif pago3.journal_id.type == 'bank' and 'Mercado pago' in pago3.journal_id.name:
                        mercadopago3 += pago3.amount
            discount = 0.0
            if sl.pricelist_id.name != 'Tarifa pública':
                for sldisc in sl.order_line:
                    discount += sldisc.product_uom_qty * (sldisc.product_id.lst_price - sldisc.price_unit)

            data_item = {'id': sl.id or '',
                         'sucursal': sl.company_id.name or '',
                         'date': date_tz,
                         'attend': sl.x_studio_selection_field_7T7lc or '',  # sl.user_id.name or '',
                         'pattient': sl.partner_id.name or '',
                         'status': status or '',
                         'studio': studio or '',
                         'tallas': sl.partner_id.x_studio_talla or '',
                         'adeudo': invoiced - paid if invoiced >= paid else 0,
                         'prod1': sl.order_line[0].product_id.name if len(sl.order_line) > 0 else '',
                         'q1': sl.order_line[0].product_uom_qty if len(sl.order_line) > 0 else 0,
                         'prod2': sl.order_line[1].product_id.name if len(sl.order_line) > 1 else '',
                         'q2': sl.order_line[1].product_uom_qty if len(sl.order_line) > 1 else 0,
                         'prod3': sl.order_line[2].product_id.name if len(sl.order_line) > 2 else '',
                         'q3': sl.order_line[2].product_uom_qty if len(sl.order_line) > 2 else 0,
                         'prod4': sl.order_line[3].product_id.name if len(sl.order_line) > 3 else '',
                         'q4': sl.order_line[3].product_uom_qty if len(sl.order_line) > 3 else 0,
                         'envio': envio or '',
                         'urgente': urgente or '',
                         'tarifa': sl.pricelist_id.name or '',
                         'desc': discount, # sl.amount_undiscounted - sl.amount_untaxed if any(slo.discount > 0 for slo in sl.order_line) else '',
                         'factura': invoice,
                         'monto_factura': sum(sl.invoice_ids.mapped('amount_total')),
                         'ajuste': '',
                         'total': '',
                         'anticipo': '',
                         'fechap1': fechap1,
                         'efectivo1': efectivo1,
                         'tarjeta1': tarjeta1,
                         'amex1': amex1,
                         'dep_transf1': dep_transf1,
                         'mercadopago1': mercadopago1,
                         'fechap2': fechap2,
                         'efectivo2': efectivo2,
                         'tarjeta2': tarjeta2,
                         'amex2': amex2,
                         'dep_transf2': dep_transf2,
                         'mercadopago2': mercadopago2,
                         'fechap3': fechap3,
                         'efectivo3': efectivo3,
                         'tarjeta3': tarjeta3,
                         'amex3': amex3,
                         'dep_transf3': dep_transf3,
                         'mercadopago3': mercadopago3,
                         'factura1': sl.invoice_ids[0].name if len(sl.invoice_ids) > 0 else '',
                         'recibo1': sl.name or '',
                         'Teléfono': 'Fijo: ' + str(sl.partner_id.phone or ' - ') + ', Celular: ' + str(
                             sl.partner_id.mobile or ' - '),
                         'E-mail': sl.partner_id.email or '',
                         'Notas paciente': sl.partner_id.comment or '',
                         'Recomienda': sl.partner_id.x_studio_cmo_nos_contacta or '',
                         'Seguimiento 20 días': '',
                         'Notas Primer Seguimiento': '',
                         'Seguimiento 90 días': '',
                         'Notas Primer Seguimiento1': '',
                         'Control seguimiento': '',
                         'Control seguimiento1': '',
                         }
            datos.append(data_item)

            # Formats
            header_plain = workbook.add_format(
                {'border': 1, 'border_color': '#000000', 'bold': True, 'font_name': 'Tahoma', 'font_color': '#0000DE',
                 'font_size': 7, 'fg_color': "#FFFF99", 'text_wrap': True, 'shrink': True, 'align': 'center',
                 'locked': True, 'valign': 'vcenter', })
            header_bold = workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 17})
            columna = workbook.add_format(
                {'border': 1, 'border_color': '#000000', 'bold': False, 'font_name': 'Tahoma', 'font_size': 8,
                 'align': 'left', 'valign': 'vcenter',
                 'locked': False, 'text_wrap': True, 'shrink': True})

            # Insertando espacio inicial
            worksheet.merge_range('A1:AS1', '')
            worksheet.set_row(0, 36)
            # Encabezados de la tabla.
            encabezado_tabla = [
                'Id',
                'Sucursal',
                'Fecha',
                'Atiende',
                'Nombre del paciente',
                'Estatus',
                'Estudio',
                'Tallas de plantillas',
                'Adeudo',
                'Prod1',
                'Q1',
                'Prod2',
                'Q2',
                'Prod3',
                'Q3',
                'Prod4',
                'q4',
                'Envío',
                'Urgente',
                'Tarifa',
                'Desc',
                'Factura Timbrada',
                'Monto factura',
                'Ajuste',
                'Total',
                'Anticipo',
                'Fecha P.1',
                'Efectivo',
                'Tarjeta',
                'AMEX',
                'Dep./transf',
                'MercadoPago',
                'Fecha P.2',
                'Efectivo',
                'Tarjeta',
                'AMEX',
                'Dep./transf',
                'MercadoPago',
                'Fecha P.3',
                'Efectivo',
                'Tarjeta',
                'AMEX',
                'Dep./transf',
                'MercadoPago',
                'Nro. Factura',
                'Recibo',
                'Teléfono',
                'E-mail',
                'Notas paciente',
                'Recomienda',
                'Seguimiento 20 días',
                'Notas Primer Seguimiento',
                'Seguimiento 90 días',
                'Notas Primer Seguimiento',
                'Control seguimiento',
                'Control seguimiento',
            ]
            # worksheet.protect()
            worksheet.write_row("A2", encabezado_tabla, header_plain)
            # Insertando datos
            row = 2
            for pos, d in enumerate(datos):
                for p, sale_dat in enumerate(d):
                    worksheet.write(row, p, d[sale_dat], columna)
                row += 1
        workbook.close()
        out.seek(0)
        generated_file = out.read()
        out.close()
        dataf = base64.encodestring(generated_file)
        self.data_file = dataf
        return {
            'name': 'Reporte de ventas',
            'view_mode': 'form',
            'view_id': False,
            'res_model': self._name,
            'domain': [],
            'context': dict(self._context, active_ids=self.ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }
