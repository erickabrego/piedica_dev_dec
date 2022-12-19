from odoo import api, fields, models

class CRMConfirmSend(models.TransientModel):
    _inherit = 'crm.confirm.send'

    x_is_branch_order = fields.Boolean(string="Orden sucursal?")

    #Se modifica el flujo para mostrar la pantalla de confirmacion
    def send_to_crm(self):
        if not self.x_is_branch_order:
            self.sale_order.sudo().write({'p_ask_for_send_to_crm':False})
            if self.sale_order.state in ["draft", "sent"]:
                self.sale_order.sudo().action_confirm()
        rec = self.sale_order
        mrp_lines = rec.order_line.filtered(lambda line: 'Fabricar' in line.product_id.route_ids.mapped('name'))
        rule_id = rec.env["branch.factory"].sudo().search([("branch_id.id", "=", rec.company_id.id)], limit=1)
        if rule_id:
            purchase_id = (rec.procurement_group_id.stock_move_ids.created_purchase_line_id.order_id | rec.procurement_group_id.stock_move_ids.move_orig_ids.purchase_line_id.order_id).ids
            purchase_id = self.env["purchase.order"].sudo().browse(purchase_id)
            purchase_id = purchase_id[0] if purchase_id else rec.sudo().create_branch_purchase_order(rule_id, mrp_lines)
            if purchase_id:
                purchase_id.write(
                    {'department_id': rule_id.department_id.id, 'partner_ref': rec.name, 'user_id': rec.user_id.id})
                purchase_id.sudo().button_confirm()
                sale = rec.sudo().create_factory_sale_order(rule_id, purchase_id, mrp_lines)
                if rec.partner_shipping_id.id != rule_id.delivery_address.id:
                    rec.picking_ids.sudo().action_cancel()
                    for line in rec.order_line:
                        purchase_line = purchase_id.order_line.filtered(lambda p_line: p_line.product_id.id == line.product_id.id)
                        for purchase in purchase_line:
                            purchase["sale_line_id"] = line.id
        if self.x_is_branch_order and not self.sale_order.x_branch_order_id.x_from_error_order:
            res = super(CRMConfirmSend, self).send_to_crm()
            return res
        elif self.x_is_branch_order and self.sale_order.x_branch_order_id.x_from_error_order:
            self.sale_order.folio_pedido = self.sale_order.x_branch_order_id.folio_pedido
            self.sale_order.estatus_crm = self.sale_order.x_branch_order_id.estatus_crm
            for history in self.sale_order.x_branch_order_id.crm_status_history:
                self.sale_order.crm_status_history = [(0,0,{'status':history.status.id,'date': history.date})]
            self.sale_order.p_ask_for_send_to_crm = False
            self.sale_order.sudo().action_confirm()
            return False

    #Se modifica la función para poder seguir el flujo de crm dentro de odoo por medio de sucursal y fabrica
    def _validate_order_data(self, data):
        if self.x_is_branch_order:
            gender = self.sale_order.x_branch_order_id.partner_id.x_studio_gnero
            data["id_paciente_odoo"] = self.sale_order.x_branch_order_id.partner_id.id
            data["id_paciente_crm"] = self.sale_order.x_branch_order_id.partner_id.id_crm
            data["datos_paciente"] = {
                'nombre': str(self.sale_order.x_branch_order_id.partner_id.name).upper(),
                'a_paterno': '',
                'a_materno': '',
                'sexo': str(dict(self.sale_order.x_branch_order_id.partner_id._fields["x_studio_gnero"].selection).get(gender)).upper(),
                'fecha_nacimiento': self.sale_order.x_branch_order_id.partner_id.x_studio_cumpleaos,
                'email': self.sale_order.x_branch_order_id.partner_id.email,
                'telefono': self.sale_order.x_branch_order_id.partner_id.phone,
                'celular': self.sale_order.x_branch_order_id.partner_id.mobile,
                'estatura': self.sale_order.x_branch_order_id.partner_id.x_studio_altura_cm,
                'peso': self.sale_order.x_branch_order_id.partner_id.x_studio_peso_kgs,
                'id_tallacalzado': float(self.sale_order.x_branch_order_id.partner_id.x_studio_talla),
                'id_sucursal': self.sale_order.x_branch_order_id.company_id.partner_id.id,
                "nombre_prescripcion": "",
                "link_prescripcion":""
            }
        res = super(CRMConfirmSend, self)._validate_order_data(data)
        return res