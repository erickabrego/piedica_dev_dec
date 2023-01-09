# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime
import requests
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_branch_order_id = fields.Many2one(comodel_name="sale.order", string="Orden sucursal", copy=False)
    x_status_error_crm = fields.Many2one(comodel_name="crm.status", string="Estado de error", copy=False)
    x_from_error_order = fields.Boolean(string="Proveniente de orden con error", copy=False)
    x_error_order = fields.Many2one(comodel_name="sale.order", string="Orden con error", copy=False)
    x_has_factory_rule = fields.Boolean(string="Regla de fabrica", compute="_get_has_factory_rule", store=True)
    x_has_error = fields.Boolean(string="Es una orden con error?", copy=False)

    #Identificamos si la compañía tiene un regla de sucursal
    @api.depends("company_id","company_id.x_is_factory")
    def _get_has_factory_rule(self):
        for rec in self:
            rule_id = rec.env["branch.factory"].sudo().search([("branch_id.id", "=", rec.company_id.id)], limit=1)
            if rule_id:
                rec.x_has_factory_rule = True
            elif rec.company_id.x_is_factory:
                rec.x_has_factory_rule = True
            else:
                rec.x_has_factory_rule = False

    #Divide las lineas de productos fabricables con una cantidad mayor a 1 al momento de crear la orden
    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        rule_id = self.env["branch.factory"].sudo().search([("branch_id.id", "=", res.company_id.id)], limit=1)
        if rule_id:
            if vals.get("order_line"):
                res._divide_in_multiple()
            res._reload_mrp_lines_sequence()
        return res


    #El historial de la sucursal es un espejo de la fabrica y divide los productos fabricables
    def write(self, values):
        res = super(SaleOrder, self).write(values)
        for rec in self:
            rule_id = rec.env["branch.factory"].sudo().search([("branch_id.id", "=", rec.company_id.id)], limit=1)
            if rule_id:
                if values.get("order_line"):
                    rec._divide_in_multiple()
                rec._reload_mrp_lines_sequence()

            if rec.x_branch_order_id:
                if values.get("estatus_crm"):
                    rec.x_branch_order_id.sudo().write({'estatus_crm': values.get("estatus_crm")})
                if values.get("crm_status_history"):
                    rec.x_branch_order_id.crm_status_history = [(5, 0, 0)]
                    for history in rec.crm_status_history.sorted(lambda line: line.date):
                        data = {
                            "status": history.status.id,
                            "date": history.date
                        }
                        rec.x_branch_order_id.crm_status_history = [(0, 0, data)]
        return res

    #Se identifica si la orden sigue el flujo de sucursal, sino el flujo es el nativo de Odoo
    def action_confirm(self):
        rule_id = self.env["branch.factory"].sudo().search([("branch_id.id", "=", self.company_id.id)], limit=1)
        if not rule_id:
            self.p_ask_for_send_to_crm = False
        return super(SaleOrder, self).action_confirm()

    #Se cancelan ambas ordenes cuando es por sucursal
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        crm_status = self.env["crm.status"].sudo().search(['|',('name','=','Cancelado'),("code", "=", "23")], limit=1)
        if self.x_branch_order_id and self.x_branch_order_id.state != 'cancel':
            self.x_branch_order_id.sudo().action_cancel()
            if not self.crm_status_history.filtered(lambda line: line.status.id == crm_status.id):
                self.estatus_crm = crm_status.id
                self.crm_status_history = [(0,0,{'status': crm_status.id, 'date': datetime.datetime.now()})]
        else:
            factory_order = self.env["sale.order"].sudo().search([("x_branch_order_id.id", "=", self.id)], limit=1)
            if factory_order and factory_order.state != 'cancel':
                factory_order.sudo().action_cancel()
                if not factory_order.crm_status_history.filtered(lambda line: line.status.id == crm_status.id):
                    factory_order.estatus_crm = crm_status.id
                    factory_order.crm_status_history = [(0,0,{'status': crm_status.id, 'date': datetime.datetime.now()})]
        return res

    #Se crea la orden de compra si es que no se tiene una regla para hacerlo
    def create_branch_purchase_order(self, rule_id, mrp_lines):
        if self.partner_id.x_studio_es_paciente and mrp_lines and rule_id:
            purchase_data = {
                "partner_id": rule_id.factory_id.partner_id.id,
                "company_id": self.company_id.id,
                "partner_ref": self.name,
                "department_id": rule_id.department_id.id,
                "user_id": self.user_id.id
            }
            purchase_id = self.env["purchase.order"].sudo().create(purchase_data)
            for order_line in mrp_lines:
                purchase_line = {
                    "product_id": order_line.product_id.id,
                    "product_qty": order_line.product_uom_qty,
                    "product_uom": order_line.product_uom.id,
                }
                purchase_id.order_line = [(0, 0, purchase_line)]
            return purchase_id

    #Se crea la orden de venta dentro de la fabrica dependiendo de la regla
    def create_factory_sale_order(self,rule_id, purchase_id, mrp_lines):
        if not self.partner_id.id_crm:
            raise ValidationError(f"El paciente {self.partner_id} no cuenta con un id de CRM, favor de sincronizar e intentar de nuevo.")
        sale_data = {
            "partner_id": self.company_id.partner_id.id,
            "partner_shipping_id": self.partner_shipping_id.id,
            "branch_id": self.company_id.partner_id.id,
            "x_studio_selection_field_waqzv": self.x_studio_selection_field_waqzv,
            "company_id": rule_id.factory_id.id,
            "team_id": False,
            "observations": self.observations,
            "user_id": self.user_id.id,
            "p_ask_for_send_to_crm": False,
            "client_order_ref": purchase_id.name,
            "payment_term_id": self.payment_term_id.id,
            "x_branch_order_id": self.id
        }
        sale_order = self.env["sale.order"].sudo().create(sale_data)

        orthopro_contact = self.env['res.partner'].search([('name', '=', 'Ortho-Pro')], limit=1)

        for order_line in mrp_lines:
            # Precio de venta de la fabrica a la sucursal
            product = order_line.product_id
            orthopro_seller = product.seller_ids.filtered(lambda seller: seller.name.id == orthopro_contact.id and seller.company_id.id == self.company_id.id)

            if not orthopro_seller:
                raise ValidationError(f'No se encontró un precio de venta de la fábrica {orthopro_contact.name} a la sucursal {self.company_id.name} para el producto {product}')

            orthopro_price = orthopro_seller.price

            if not orthopro_price:
                raise ValidationError(f'No se encontró un precio de venta de la fábrica {orthopro_contact.name} a la sucursal {self.company_id.name} para el producto {product}')

            sale_line = {
                "product_id": order_line.product_id.id,
                "product_uom_qty": order_line.product_uom_qty,
                "product_uom": order_line.product_uom.id,
                "insole_size": order_line.insole_size,
                "top_cover_id": order_line.top_cover_id.id,
                "design_type": order_line.design_type,
                "analytic_tag_ids": order_line.analytic_tag_ids.ids,
                "main_layer_id": order_line.main_layer_id.id,
                "mid_layer_id": order_line.mid_layer_id.id,
                "x_shapelist_domian_ids": order_line.x_shapelist_domian_ids.id,
                "price_unit": orthopro_price,
            }
            sale_order.order_line = [(0,0,sale_line)]

        confirme_send_obj = self.env["crm.confirm.send"].sudo().create({"sale_order": sale_order.id, "x_is_branch_order":True})
        notification = confirme_send_obj.sudo().send_to_crm()
        if notification and notification['params']['type'] == 'success' and not self.x_from_error_order:
            self.folio_pedido = sale_order.folio_pedido
            self.estatus_crm = sale_order.estatus_crm
        return notification

    #Renvio de información
    def resend_to_crm(self):
        mrp_lines = self.order_line.filtered(
                lambda line: 'Fabricar' in line.product_id.route_ids.mapped('name') and line.product_uom_qty == 1)
        if mrp_lines:
            crm_confirm_obj = self.env["crm.confirm.send"].create({'sale_order': self.id})
            return crm_confirm_obj.send_to_crm()
        else:
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ("Error al reenviar el pedido"),
                    'message': "No existen productos fabricables dentro de la orden.",
                    'type': 'warning',
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
            return notification

    def send_error_to_crm(self):
        if self.order_line.filtered(lambda line: line.x_is_error_line):
            crm_status = self.env["crm.status"].sudo().search(['|',('name','=','Error'),("code", "=", "2")], limit=1)
            url = f"https://crmpiedica.com/api/api.php?id_pedido={self.folio_pedido}&id_etapa={crm_status.id}"
            token = self.env['ir.config_parameter'].sudo().get_param("crm.sync.token")
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
            response = requests.put(url, headers=headers)

            if self.x_branch_order_id:
                self.send_crm_status_factory(self, response, crm_status)
                self.x_has_error = True
                self.x_branch_order_id.x_has_error = True
                self._send_error_with_mo_crm(self)
            else:
                factory_order = self.env["sale.order"].sudo().search([("x_branch_order_id.id", "=", self.id)], limit=1)
                if factory_order:
                    self.send_crm_status_factory(factory_order, response, crm_status)
                    factory_order.x_has_error = True
                    self._send_error_with_mo_crm(factory_order, from_branch=True)
                self.x_has_error = True
        else:
            raise ValidationError("No es posible de marcar como error la orden, debido a que no se cuenta con productos con errores.")

    def _send_error_with_mo_crm(self, order, from_branch=False):
        url = f"https://crmpiedica.com/api/api.php"
        token = self.env['ir.config_parameter'].sudo().get_param("crm.sync.token")
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        data = [
            {
                'id_pedido_crm': order.folio_pedido,
                'observaciones': order.x_branch_order_id.observations if from_branch else order.observations,
                'productos_error': []
            }
        ]
        mrp_orders = self.env['mrp.production'].sudo().search([('origin', '=', order.name)])
        mrp_orders_list = []
        error_lines = order.x_branch_order_id.order_line.filtered(lambda line: line.x_is_error_line)

        for branch_error_line in error_lines:
            factory_line = self.env["sale.order.line"].sudo().search([('order_id.id','=',order.id),('product_id.id','=',branch_error_line.product_id.id),('x_is_error_line','=',False)],limit=1)
            factory_line.x_is_error_line = True

        error_mo = mrp_orders.filtered(lambda mo: mo.product_id.id in error_lines.mapped('product_id.id'))
        if error_mo:
            for mrp_order in error_mo:
                mrp_orders_list.append({
                    'id_mo_odoo': mrp_order.id,
                })
            data[0]['productos_error'] = mrp_orders_list

        #Enviar error a CRM junto con las MO
        _logger.info('===================ENVIO DE ERROR=================')
        _logger.info(data)
        _logger.info('--------------------------------------------------')
        response = requests.put(url, headers=headers, json=data)
        order.message_post(body=f"{response.content.decode('utf-8')}")
        order.x_branch_order_id.message_post(body=f"{response.content.decode('utf-8')}")


    #Copiamos la orden de venta y se confirmar sin generar otra venta en crm
    def copy_error_order(self, kwargs):
        error_id = kwargs.get("error_id",None)
        status_id = kwargs.get("estatus_crm",None)
        error_status = self.env["crm.status"].sudo().search([('code', '=', str(error_id))], limit=1)
        if error_id == 12:
            pricelist_id = self.env["product.pricelist"].sudo().search([('id','=',80)])
            error_status = self.env["crm.status"].sudo().search([('code', '=', str(error_id))], limit=1)
        if not status_id:
            raise ValidationError("Favor de proporcionar el id estatus de crm.")
        else:
            crm_status = self.env["crm.status"].sudo().search([('code','=',str(status_id))],limit=1)
            if not crm_status:
                raise ValidationError("No se encuentra en la base de datos el id proporcionado.")
        if error_status:
            self.sudo().write({'estatus_crm': error_status.id})
            self.sudo().create_estatus_crm()
        sale_order_id = self.sudo().copy()
        branch_order = self.x_branch_order_id.sudo().copy()
        sale_order_id.x_branch_order_id = branch_order.id

        branch_error_lines = branch_order.order_line.filtered(lambda line: line.x_is_error_line)

        for order_line in sale_order_id.order_line:
            order_line.x_is_error_line = False

        for branch_error_line in branch_error_lines:
            factory_line = self.env["sale.order.line"].sudo().search([('order_id.id','=',sale_order_id.id),('product_id.id','=',branch_error_line.product_id.id),('x_is_error_line','=',False)],limit=1)
            factory_line.x_is_error_line = True if factory_line else False

        error_lines = sale_order_id.order_line.filtered(lambda line: not line.x_is_error_line)
        branch_error_lines = branch_order.order_line.filtered(lambda line: not line.x_is_error_line)

        for error_line in error_lines:
            sale_order_id.order_line = [(2,error_line.id)]
        for branch_error_line in branch_error_lines:
            branch_order.order_line = [(2, branch_error_line.id)]

        sale_order_id.x_error_order = self.id
        branch_order.x_error_order = self.x_branch_order_id.id
        sale_order_id.folio_pedido = self.folio_pedido
        branch_order.folio_pedido = self.folio_pedido


        sale_order_id.x_from_error_order = True
        branch_order.x_from_error_order = True
        sale_order_id.estatus_crm = crm_status.id
        branch_order.estatus_crm = crm_status.id
        sale_order_id.crm_status_history = [(0,0,{'status': crm_status.id, 'date': datetime.datetime.now()})]

        sale_order_id.sudo().action_confirm()
        branch_order.sudo().action_confirm()

        if pricelist_id:
            if sale_order_id.x_branch_order_id:
                sale_order_id.x_branch_order_id.pricelist_id = pricelist_id.id
                sale_order_id.x_branch_order_id.update_prices()
                sale_order_id.pricelist_id = pricelist_id.id
                sale_order_id.update_prices()
            else:
                factory_order = self.env["sale.order"].sudo().search([("x_branch_order_id","=",sale_order_id.id)],limit=1)
                if factory_order:
                    factory_order.pricelist_id.id = pricelist_id.id
                    factory_order.update_prices()
                sale_order_id.pricelist_id = pricelist_id.id
                sale_order_id.update_prices()

        mrp_orders = self.env['mrp.production'].sudo().search([('origin', '=',sale_order_id.name)])
        mrp_orders_list = []

        res = {
            'status': 'success',
            'content': {
                'sale_order': {
                    'id': sale_order_id.id,
                    'name': sale_order_id.name
                }

            }
        }
        if mrp_orders:
            for mrp_order in mrp_orders:
                mrp_orders_list.append({
                    'id': mrp_order.id,
                    'name': mrp_order.name,
                    'product_id': mrp_order.product_id.id
                })
            res['content']['mrp_orders'] = mrp_orders_list
        return res

    #Actualiza los status de crm en Odoo tanto para la sucursal y fabrica
    def send_crm_status_factory(self, sale_id, response, crm_status):
        sale_id.sudo().message_post(body=response.content)
        sale_id.sudo().write({'estatus_crm': crm_status.id})
        sale_id.sudo().create_estatus_crm()
