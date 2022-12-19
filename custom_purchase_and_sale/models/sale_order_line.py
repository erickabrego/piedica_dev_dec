from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    x_shapelist_domian_ids = fields.Many2one(comodel_name="prod.shape.list", string="Lista de molde")
    x_is_custom = fields.Boolean(string="Es custom", related="product_id.is_custom")
    x_is_error_line = fields.Boolean(string="Con error?", copy=True)

    @api.onchange("product_id")
    def _get_shapelist_domain(self):
        for rec in self:
            if rec.product_id:
                return {'domain': {'x_shapelist_domian_ids': [('id', 'in', rec.product_id.prod_shape_list_ids.ids)]}}

    @api.onchange("product_id")
    def _get_layers_domain(self):
        for rec in self:
            if rec.product_id:
                rule_id = rec.env["branch.factory"].sudo().search([("branch_id.id", "=", rec.company_id.id)], limit=1)
                if rule_id:
                    main_layer_ids = rec.env["product.product"].with_company(rule_id.factory_id.id).search([("is_material","=",True),("matMainLayer","=",True),("qty_available",">",0)])
                    top_layer_ids = rec.env["product.product"].with_company(rule_id.factory_id.id).search([("is_material", "=", True), ("matTopLayer", "=", True), ("qty_available", ">", 0)])
                    mid_layer_ids = rec.env["product.product"].with_company(rule_id.factory_id.id).search([("is_material", "=", True), ("matMidLayer", "=", True), ("qty_available", ">", 0)])
                    return {'domain': {'top_cover_id': [('id', 'in', top_layer_ids.ids)], 'main_layer_id': [('id','in',main_layer_ids.ids)], 'mid_layer_id':[('id','in',mid_layer_ids.ids)]}}
