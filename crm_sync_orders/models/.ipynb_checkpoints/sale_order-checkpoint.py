import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    branch_id = fields.Many2one('res.partner', string='Sucursal', domain=lambda self: [('category_id', '=', self.env['res.partner.category'].sudo().search([('name', '=', 'Sucursal')]).id)])
    estatus_crm = fields.Many2one('crm.status', string='Estatus CRM', readonly=True, copy=False)
    folio_pedido = fields.Char('Folio del pedido', readonly=True, copy=False)
    crm_status_history = fields.One2many('crm.status.history', 'sale_order', string='Historial de estatus', readonly=True, copy=False)
    observations = fields.Text(string='Observaciones')
    x_studio_selection_field_waqzv = fields.Selection([('Adicional','Adicional'),('PSA', 'PSA'),('Primera Orden','Primera Orden'),('PSA Mismo Proyecto','PSA Mismo Proyecto'),('PSI','PSI'),('Segunda Orden','Segunda Orden'),('Otros','Otros'),('Error','Error')], string='Tipo pedido')
    p_ask_for_send_to_crm = fields.Boolean(default=True, copy=False)
    is_adjustment = fields.Boolean(string="Es ajuste", default=False)

    #Divide las lineas de productos fabricables con una cantidad mayor a 1 al momento de crear la orden
    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if vals.get("order_line"):
            res._divide_in_multiple()
        return res

    # Divide las lineas de productos fabricables con una cantidad mayor a 1 al momento de editar la orden
    def write(self, values):
        res = super(SaleOrder, self).write(values)
        if values.get("order_line"):
            self._divide_in_multiple()
        return res

    #Divide lineas en cantidades unitarias aquellos productos fabricables
    def _divide_in_multiple(self):
        for rec in self:
            mrp_lines = rec.order_line.filtered(lambda line: 'Fabricar' in line.product_id.route_ids.mapped('name') and line.product_uom_qty > 1)
            for mrp_line in mrp_lines:
                for quantity in range(int(mrp_line.product_uom_qty) - 1):
                    mrp_line.copy(default={'order_id': rec.id, 'product_uom_qty': 1})
                mrp_line.update({'product_uom_qty': 1})

    def create_crm_order(self, data):
        order_line = data.pop('order_line')
        sale_order = self.with_context(lang='es_MX').create(data)
        order_line_status = sale_order.create_crm_order_line(order_line)

        if order_line_status['status'] == 'error':
            return order_line_status

        try:
            # Se desactiva la opción de mandar a CRM, ya uqe eso solo es con las
            # órdenes creadas desde Odoo
            sale_order.write({'p_ask_for_send_to_crm': False})
            sale_order.action_confirm()
        except UserError as e:
            return  {
                'status': 'error',
                'message': e.args[0]
            }


        sale_order.create_estatus_crm()

        res = {
            'status': 'success',
            'content': {
                'sale_order': {
                    'id': sale_order.id,
                    'name': sale_order.name
                }

            }
        }

        procurement_groups = self.env['procurement.group'].sudo().search([('sale_id', 'in', sale_order.ids)])
        mrp_orders = procurement_groups.stock_move_ids.created_production_id
        mrp_orders_list = []

        if mrp_orders:
            for mrp_order in mrp_orders:
                mrp_orders_list.append({
                    'id': mrp_order.id,
                    'name': mrp_order.name,
                    'product_id': mrp_order.product_id.id
                })

            res['content']['mrp_orders'] = mrp_orders_list

        return res



    def create_crm_order_line(self, products):
        self.ensure_one()
        sale_order_line_obj = self.env['sale.order.line']
        product_product_obj = self.env['product.product']

        for product_data in products:
            product = product_product_obj.sudo().search([('id', '=', product_data['id'])])

            line_data = {
                'name': product.name,
                'product_id': product.id,
                'product_uom': product.uom_id.id if product.uom_id else False,
                'order_id': self.id,
                'product_uom_qty': product_data['quantity'],
                'insole_size': product_data['insole_size']
            }

            sale_order_line_obj.create(line_data)

        return {
            'status': 'success'
        }


    def create_estatus_crm(self):
        self.ensure_one()
        self.write({
            'crm_status_history': [(0, 0, {
                'sale_order': self.id,
                'status': self.estatus_crm.id,
                'date': datetime.datetime.now()
            })]
        })


    def update_estatus_crm(self, data):
        self.ensure_one()

        self.write({'estatus_crm': self.env['crm.status'].sudo().search([('code', '=', data['estatus_crm'])])[0].id})
        self.create_estatus_crm()

        if data['add_materials']:
            self.update_manufacturing_order(data['mrp_orders'])

        elif data['is_send']:
            self.update_delivery_order()

        return {
            'status': 'success'
        }


    def update_manufacturing_order(self, mrp_orders):
        self.ensure_one()

        context = {
            'active_id': self.id,
            'active_ids': [self.id],
            'active_model': 'sale.order',
            'allowed_company_ids': [self.company_id.id]
        }

        for mrp_order_data in mrp_orders:
            mrp_order = self.env['mrp.production'].with_context(context).browse(mrp_order_data['id'])

            # Verifica si es un ajuste
            is_adjustment = mrp_order_data.get('adjustment', None)
            

            if is_adjustment:
                mrp_bom = self.env['mrp.bom'].sudo().search([
                    ('product_tmpl_id', '=', mrp_order.product_tmpl_id.id),
                    ('code', '=', 'Ajuste')
                ],limit=1)
            else:
                mrp_bom = self.env['mrp.bom'].sudo().search([
                    ('product_tmpl_id.id', '=', mrp_order.product_tmpl_id.id),
                ],limit=1)

            # Materiales del producto
            components_data = []

            for component_data in mrp_order_data['components']:
                component = self.env['product.product'].browse(component_data['id'])
                warehouse_id = self.env["stock.warehouse"].sudo().search([("lot_stock_id.id","=",mrp_order.location_src_id.id)],limit=1)

                components_data.append((0, 0, {
                    'name': component.name,
                    'product_id': component.id,
                    'product_uom': component.uom_id.id if component.uom_id else False,
                    'raw_material_production_id': mrp_order.id,
                    'product_uom_qty': component_data['quantity'],
                    #'quantity_done': component_data['quantity'],
                    'company_id': self.company_id.id,
                    'location_id': mrp_order.location_src_id.id,
                    'location_dest_id': mrp_order.production_location_id.id,
                    'warehouse_id': warehouse_id.id,
                    'picking_type_id': mrp_order.picking_type_id.id
                }))



            # Hay que rehacer las órdenes de trabajo dado que la lista de
            # materiales muy probablemente haya cambiado
            mrp_order.workorder_ids.unlink()
            mrp_order.write({'bom_id': mrp_bom.id,})
            mrp_order._onchange_workorder_ids()

            mrp_order.write({'move_raw_ids': components_data})
            mrp_order.action_confirm()
            #mrp_order.button_mark_done()


    def update_delivery_order(self):
        self.ensure_one()

        context = {
            'active_id': self.id,
            'active_ids': [self.id],
            'active_model': 'sale.order',
            'allowed_company_ids': [self.company_id.id]
        }

        delivery_orders = self.env['stock.picking'].with_context(context).sudo().search([('origin', '=', self.name)])

        for delivery_order in delivery_orders:
            for line in delivery_order.move_line_ids_without_package:
                line.write({'qty_done': line.product_uom_qty})

            try:
                delivery_order.p_button_validate()                
            except UserError as e:
                return  {
                    'status': 'error',
                    'message': e.args[0]
                }


    def action_confirm(self):
        # Cuando una orden se confirme, la información de la orden se enviará a
        # CRM, pero es necesario primero mostrar una alerta para informar y
        # confirmar que dicha acción se llevará a cabo, ya que la información
        # solo se podrá enviar una vez. Dicha funcionalidad se llevará a cabo
        # mediante un wizard y solo si se trabaja con productos fabricables
        mrp_lines = self.order_line.filtered(lambda line: 'Fabricar' in line.product_id.route_ids.mapped('name') and line.product_uom_qty == 1)
        if self.p_ask_for_send_to_crm and mrp_lines:
            view = self.env.ref('crm_sync_orders.view_crm_confirm_send')
            return {
                'name': '¿Confirmar y enviar a CRM?',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'crm.confirm.send',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': dict(self.env.context, default_sale_order=self.id)
            }
        return super().action_confirm()
    
    #Renvio de información
    def resend_to_crm(self):        
        crm_confirm_obj = self.env["crm.confirm.send"].create({'sale_order':self.id})        
        return crm_confirm_obj._send_data()
