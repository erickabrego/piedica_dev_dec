from odoo import models, fields

class StatusHistory(models.Model):
    _name = 'crm.status.history'
    _description = 'Historial de status'
    _order = 'id desc'


    sale_order = fields.Many2one('sale.order', ondelete='cascade', string='Orden de venta', required=True, readonly=True)
    status = fields.Many2one('crm.status', string='Estatus', readonly=True)
    date = fields.Datetime('Fecha', readonly=True)
