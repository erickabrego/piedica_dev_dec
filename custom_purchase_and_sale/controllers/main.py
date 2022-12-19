from odoo.http import Controller, request, route, Response
import logging
import json
_logger = logging.getLogger(__name__)


class MainController(Controller):

    #Crear una copia de la orden de venta cuando esta tiene error
    @route('/sync-error-orders/<id>', type='json', auth='none')
    def copy_error_order(self, id, **kwargs):
        response = []
        if not str(id).isnumeric():
            response.append({
                'status': 'error',
                'message': 'El id de la orden de venta debe ser un valor numérico. Valor introducido: %s' % str(id)
            })
        order = request.env['sale.order'].sudo().search([('id', '=', id),('x_branch_order_id','!=',False)])
        if not order:
            response.append({
                'status': 'error',
                'message': 'No se encontró la orden de venta con el id %s' % id
            })
        else:
            copy_order = order.sudo().copy_error_order(kwargs)
            if copy_order:
                response = copy_order
            else:
                response.append({
                    'status': 'error',
                    'message': f'No fue posible crear la nueva orden a partir del error.'
                })
        return response

