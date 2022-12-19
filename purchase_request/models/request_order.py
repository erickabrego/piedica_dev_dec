# -*- coding: utf-8 -*-

from datetime import datetime, time

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class RequestOrderPurchase(models.Model):
    _name = 'request.order.purchase'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Request Order"
    _rec_name = 'code'

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })


    READONLY_STATES = {
        'published': [('readonly', True)],
        'approved': [('readonly', True)],
        'rejected': [('readonly', True)],
    }

    code = fields.Char('Code', required=True, index=True, copy=False, default='New')
    partner_id = fields.Many2one('res.partner', string='Vendor', required=False, states=READONLY_STATES,
                                 tracking=True,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    date_order = fields.Datetime('Date order', required=True, states=READONLY_STATES, index=True, copy=False,
                                 default=fields.Datetime.now)
    department_id = fields.Many2one('hr.department', 'Department', store=True)

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES,
                                 default=lambda self: self.env.company.id)
    user_id = fields.Many2one(
        'res.users', string='Purchase Representative', index=True, tracking=True,
        default=lambda self: self.env.user, check_company=True)
    currency_id = fields.Many2one('res.currency', 'Currency', required=False, states=READONLY_STATES,
                                  default=lambda self: self.env.company.currency_id.id)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     tracking=True)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('published', 'Published'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', readonly=True, copy=False, index=True, default='draft', tracking=True)
    order_line = fields.One2many('request.order.purchase.line', 'order_id', string='Products',
                                 states={'published': [('readonly', True)],
                                         'approved': [('readonly', True)],
                                         'rejected': [('readonly', True)]}, copy=True
                                 )
    product_id = fields.Many2one('product.product', related='order_line.product_id', string='Product', readonly=False)
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position',
                                         domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    order_ids = fields.One2many('purchase.order', 'req_order_id', 'Purchase Order')
    count_order = fields.Integer('Quantity of orders', compute='_compute_count_order')
    employee_id = fields.Many2one("hr.employee", string="Beneficiario")
    company_ids = fields.Many2many('res.company', compute='_compute_companies',
                                   string='Compañía permitidas')
    purchase_address_id = fields.Many2one("purchase.address", 'Lugar de entrega')

    @api.depends('user_id')
    def _compute_companies(self):
        if self.user_id:
            self.company_ids = self.user_id.company_ids

    @api.constrains('order_line', 'state')
    def _check_order_line(self):
        for order in self:
            order_lines = order.order_line
            if len(order_lines) == 0:
                raise ValidationError(_('No hay líneas de productos creada. Debe haber al menos una.'))

    def action_apply_lines(self):
        partner_id = self.partner_id.id
        self.order_line.res_partner_id = partner_id

    def _check_access_right(self, group):
        if self.env['res.users'].has_group(group):
            return True
        return False

    def action_confirm(self):
        return self.write({'state': 'published'})

    def action_to_approve(self):
        if not self._check_access_right('purchase.group_purchase_manager'):
            raise UserError(
                _('Sorry you do not have permission to perform the required operation.\n'
                  'If you think it is an mistake,please contact the Administrator.'))

        return self.write({'state': 'approved'})

    def action_reject(self):
        if not self._check_access_right('purchase.group_purchase_manager'):
            raise UserError(
                _('Sorry you do not have permission to perform the required operation.\n'
                  'If you think it is an mistake,please contact the Administrator.'))

        return self.write({'state': 'rejected'})

    @api.model
    def create(self, vals):
        company_id = vals.get('company_id')
        self_comp = self.with_company(company_id)
        if vals.get('code', 'New') == 'New':
            vals['code'] = self_comp.env['ir.sequence'].next_by_code('request.order.purchase')
        return super(RequestOrderPurchase, self_comp).create(vals)

    def unlink(self):
        for order in self:
            if not order.state == 'draft':
                raise UserError(_('In order to delete a purchase order, it must be in draft state.'))
        return super(RequestOrderPurchase, self).unlink()

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        # Ensures all properties and fiscal positions
        # are taken with the company of the order
        # if not defined, with_company doesn't change anything.
        self = self.with_company(self.company_id)
        if not self.partner_id:
            self.fiscal_position_id = False
            self.currency_id = self.env.company.currency_id.id
        else:
            self.fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id)
            self.currency_id = self.partner_id.property_purchase_currency_id.id or self.env.company.currency_id.id
        return {}

    @api.onchange('fiscal_position_id', 'company_id')
    def _compute_tax_id(self):
        """
        Trigger the recompute of the taxes if the fiscal position is changed on the PO.
        """
        self.order_line._compute_tax_id()

    @api.depends('order_ids.state')
    def _compute_count_order(self):
        for record in self:
            record.count_order = len(record.order_ids)

    def action_view_purchase(self):
        if not self._check_access_right('purchase.group_purchase_manager'):
            raise UserError(
                _('Sorry you do not have permission to perform the required operation.\n'
                  'If you think it is an mistake,please contact the Administrator.'))

        action = self.env["ir.actions.actions"]._for_xml_id(
            "purchase.purchase_form_action"
        )
        action["context"] = {
            "search_default_req_order_id": self.id,
            "default_req_order_id": self.id,
            "default_department_id": self.department_id.id if self.department_id else False,
        }
        action["domain"] = [
            ('state', 'in', ('purchase', 'done')), ('req_order_id', '=', self.id)
        ]
        order_ids = self.order_ids

        if len(order_ids) == 1:
            action["views"] = [
                (
                    self.env.ref(
                        "purchase_request.purchase_order_inherit_ext_form"
                    ).id,
                    "form",
                )
            ]
            action["res_id"] = order_ids.id
        return action


class RequestOrderPurchaseLine(models.Model):
    _name = 'request.order.purchase.line'
    _inherit = 'purchase.order.line'
    _description = 'Products Line'
    _order = 'order_id, id'

    order_id = fields.Many2one('request.order.purchase', string='Request Order', index=True, ondelete='cascade')
    res_partner_id = fields.Many2one('res.partner', string='Partner', readonly=False,
                                     domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    def _compute_qty_received(self):
        for line in self:
            line.qty_received = 0.0

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        if not self.product_id:
            return
        params = {'order_id': self.order_id}
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order.date(),
            uom_id=self.product_uom,
            params=params)

        if seller or not self.date_planned:
            self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        # If not seller, use the standard price. It needs a proper currency conversion.
        if not seller:
            po_line_uom = self.product_uom or self.product_id.uom_po_id
            price_unit = self.env['account.tax']._fix_tax_included_price_company(
                self.product_id.uom_id._compute_price(self.product_id.standard_price, po_line_uom),
                self.product_id.supplier_taxes_id,
                self.taxes_id,
                self.company_id,
            )
            if price_unit and self.order_id.currency_id and self.order_id.company_id.currency_id != self.order_id.currency_id:
                price_unit = self.order_id.company_id.currency_id._convert(
                    price_unit,
                    self.order_id.currency_id,
                    self.order_id.company_id,
                    self.date_order or fields.Date.today(),
                )

            self.price_unit = price_unit
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price,
                                                                             self.product_id.supplier_taxes_id,
                                                                             self.taxes_id,
                                                                             self.company_id) if seller else 0.0
        if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit

    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity', 'qty_received', 'product_uom_qty',
                 'order_id.state')
    def _compute_qty_invoiced(self):
        for line in self:
            if line._table == 'request_order_purchase_line':
                line.qty_invoiced = 0
                line.qty_to_invoice = 0


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('analytic_tag_ids')
    def _onchange_analytic_tag_ids_one(self):
        for record in self:
            if len(self.analytic_tag_ids) > 1:
                raise ValidationError('Solo debe ser un Centro de costo por cada linea de producto.')
