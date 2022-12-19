from odoo import http, fields
from odoo.http import Controller, request, route, Response
from odoo.exceptions import UserError
import json

class MainController(Controller):

    #Endpoint obtener recubrimientos y materiales
    @route('/get-products', type='http', auth='none')
    def get_materials(self):
        #Obtener materiales
        materials = request.env['product.product'].sudo().with_company(6).search([("is_material","=",True),("matTopLayer", "=", False)])
        material_list = []
        response = [{'materiales': material_list}]
        for material in materials:
            qty = sum(request.env["stock.quant"].sudo().with_company(6).search([("location_id.usage","=","internal"),("product_id.id","=",material.id)]).mapped("available_quantity"))
            if qty > 0:
                data = {
                    "nombre": material.display_name,
                    "id": material.id,
                    "qty": qty
                }
                response[0]["materiales"].append(data)
        #Obtener recubrimientos
        topcovers = request.env['product.product'].sudo().with_company(6).search([("is_material","=",True),("matTopLayer", "=", True)])
        topcover_list = []
        response.append({'recubrimientos': topcover_list})
        for topcover in topcovers:
            qty = sum(request.env["stock.quant"].sudo().with_company(6).search([("location_id.usage","=","internal"),("product_id.id","=",topcover.id)]).mapped("available_quantity"))
            if qty > 0:
                data = {
                    "nombre": topcover.display_name,
                    "id": topcover.id,
                    "qty": qty
                }
                response[1]["recubrimientos"].append(data)
        return json.dumps(response, indent=2)


    @route('/sync-orders', type='json', auth='none')
    def create_orders(self, **kwargs):
        sale_order_obj = request.env['sale.order'].sudo()
        args_status = self.validate_create_data(kwargs)
        if args_status['status'] == 'error':
            return args_status
        result = sale_order_obj.create_crm_order(args_status['content'])
        return result


    @route('/sync-orders/<id>', type='json', auth='none')
    def edit_orders(self, id, **kwargs):
        if not str(id).isnumeric():
            return {
                'status': 'error',
                'message': 'El id de la orden de venta debe ser un valor numérico. Valor introducido: %s' % str(id)
            }
        order = request.env['sale.order'].sudo().search([('id', '=', id)])
        if not order:
            return {
                'status': 'error',
                'message': 'No se encontró la orden de venta con el id %s' % id
            }
        args_status = self.validate_update_data(kwargs, int(id))
        if args_status['status'] == 'error':
            return args_status

        result = order.update_estatus_crm(args_status['content'])
        return result

    def validate_create_data(self, args):
        product_product_obj = request.env['product.product'].sudo()

        customer = args.get('customer', None) # partner_id - Cliente
        branch = args.get('branch', None) # branch - Sucursal
        invoice_address = args.get('invoice_address', None) # partner_invoice_id - Dirección de factura
        delivery_address = args.get('delivery_address', None) # partner_shipping_id - Dirección de entrega
        pricelist = args.get('pricelist', None) # pricelist_id - Lista de precios
        payment_terms = args.get('payment_terms', None) # payment_term_id - Términos de pago
        tipo_pedido = args.get('tipo_pedido', None) # x_studio_selection_field_waqzv - Tipo de pedido
        estatus_crm = args.get('estatus_crm', None) # estatus_crm - Estatus CRM
        folio_pedido = args.get('folio_pedido', None) # folio_pedido - Folio pedido
        ajuste = args.get('is_adjustment', None) # is_adjustment - Es ajuste?
        order_line = args.get('order_line', None) # order_line - Línea de la orden
        salesperson = args.get('salesperson', None) # user_id - Vendedor
        sales_team = args.get('sales_team', None) # team_id - Equipo de ventas
        company = args.get('company', None) # company_id - Empresa
        online_signature = args.get('online_signature', None) # require_signature - Firma en línea
        shipping_policy = args.get('shipping_policy', None) # picking_policy - Política de entrega
        observations = args.get('observations', None)
        missing_args = []

        # Comprueba que se hayan suplido todos los argumentos
        if not customer:
            missing_args.append('customer')
        else:
            if not isinstance(customer, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro customer debe ser un valor numérico. Valor introducido: %s' % str(customer)
                }

            customer_record = request.env['res.partner'].sudo().search([('id', '=', customer)])

            if not customer_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró el cliente con el id %s' % customer
                }

        if not branch:
            missing_args.append('branch')
        else:
            if not isinstance(branch, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro branch debe ser un valor numérico. Valor introducido: %s' % str(customer)
                }

            branch_record = request.env['res.partner'].sudo().search([('id', '=', branch)])

            if not branch_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró la sucursal con el id %s' % branch
                }

        if not invoice_address:
            missing_args.append('invoice_address')
        else:
            if not isinstance(invoice_address, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro invoice_address debe ser un valor numérico. Valor introducido: %s' % str(invoice_address)
                }

            invoice_address_record = request.env['res.partner'].sudo().search([('id', '=', customer)])

            if not invoice_address_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró la dirección de facturación con el id %s' % invoice_address_record
                }

        if not delivery_address:
            missing_args.append('delivery_address')
        else:
            if not isinstance(delivery_address, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro delivery_address debe ser un valor numérico. Valor introducido: %s' % str(delivery_address)
                }

            delivery_address_record = request.env['res.partner'].sudo().search([('id', '=', delivery_address)])

            if not delivery_address_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró la dirección de facturación con el id %s' % invoice_address_record
                }


        if not pricelist:
            missing_args.append('pricelist')
        else:
            if not isinstance(pricelist, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro pricelist debe ser un valor numérico. Valor introducido: %s' % str(pricelist)
                }
            pricelist_record = request.env['product.pricelist'].sudo().search([('id', '=', pricelist)])

            if not pricelist_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró la lista de precios con el id %s' % pricelist
                }

        if not payment_terms:
            missing_args.append('payment_terms')
        else:
            if not isinstance(payment_terms, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro payment_terms debe ser un valor numérico. Valor introducido: %s' % str(payment_terms)
                }

            payment_terms_record = request.env['account.payment.term'].sudo().search([('id', '=', payment_terms)])

            if not payment_terms_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró el término de pago con el id %s' % payment_terms
                }

        if not tipo_pedido:
            missing_args.append('tipo_pedido')
        else:
            if not isinstance(tipo_pedido, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro tipo_pedido debe ser un string. Valor introducido: %s' % str(tipo_pedido)
                }

            tipo_pedido_val = dict(request.env['sale.order'].sudo()._fields['x_studio_selection_field_waqzv'].selection).get(tipo_pedido, None)

            if not tipo_pedido_val:
                return {
                    'status': 'error',
                    'message': 'No se encontró el valor %s para el tipo de pedido' % tipo_pedido
                }


        if not estatus_crm:
            missing_args.append('estatus_crm')
        else:
            if not isinstance(estatus_crm, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro estatus_crm debe ser un valor numérico. Valor introducido: %s' % str(estatus_crm)
                }
            

            estatus_crm_record = request.env['crm.status'].sudo().search([('code', '=', str(estatus_crm))],limit=1)
            

            if not estatus_crm_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró el estatus con el id %s' % estatus_crm
                }


        if not folio_pedido:
            missing_args.append('folio_pedido')
        else:
            if not isinstance(folio_pedido, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro folio_pedido debe ser un string. Valor introducido: %s' % str(folio_pedido)
                }

        if not order_line:
            missing_args.append('order_line')
        else:
            if not isinstance(order_line, list):
                return {
                    'status': 'error',
                    'message': 'El parámetro order_line debe ser un array. Valor introducido: %s' % str(order_line)
                }

        if not salesperson:
            missing_args.append('salesperson')
        else:
            if not isinstance(salesperson, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro salesperson debe ser un string. Valor introducido: %s' % str(salesperson)
                }

            salesperson_record = request.env['res.users'].sudo().search([('email', '=', salesperson)])

            if not salesperson_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró el vendedor con el email %s' % salesperson
                }
            else:
                salesperson = salesperson_record.id

        if not sales_team:
            missing_args.append('sales_team')
        else:
            if not isinstance(sales_team, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro sales_team debe ser un valor numérico. Valor introducido: %s' % str(sales_team)
                }

            sales_team_record = request.env['crm.team'].sudo().search([('id', '=', sales_team)])

            if not sales_team_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró el equipo de ventas con el id %s' % sales_team
                }

        if not company:
            missing_args.append('company')
        else:
            if not isinstance(company, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro company debe ser un valor numérico. Valor introducido: %s' % str(company)
                }

            company_record = request.env['res.company'].sudo().search([('id', '=', company)])

            if not company_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró la compañía con el id %s' % company
                }

        if online_signature == None:
            missing_args.append('online_signature')
        else:
            if not isinstance(online_signature, bool):
                return {
                    'status': 'error',
                    'message': 'El parámetro online_signature debe ser un valor booleano. Valor introducido: %s' % str(online_signature)
                }

        if not shipping_policy:
            missing_args.append('shipping_policy')
        else:
            if not isinstance(shipping_policy, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro shipping_policy debe ser un string. Valor introducido: %s' % str(shipping_policy)
                }

            shipping_policy_val = dict(request.env['sale.order'].sudo()._fields['picking_policy'].selection).get(shipping_policy, None)

            if not shipping_policy_val:
                return {
                    'status': 'error',
                    'message': 'No se encontró el valor %s para shipping_policy' % shipping_policy
                }

        if not observations:
            missing_args.append('observations')
        else:
            if not isinstance(observations, str):
                return {
                    'status': 'error',
                    'message': 'El parámetro observations debe ser un string. Valor introducido: %s' % str(observations)
                }


        if missing_args:
            return {
                'status': 'error',
                'message': 'Faltan los siguientes argumentos: %s' % ', '.join(missing_args)
            }


        if len(order_line) == 0:
            return {
                'status': 'error',
                'message': 'La linea de la orden no tiene ningun producto asignado'
            }

        # Comprueba que los productos existan en Odoo
        line_count = 1
        for product_data in order_line:
            line_missing_args = []

            if not 'id' in product_data:
                line_missing_args.append('id')
            else:
                if not isinstance(product_data['id'], int):
                    return {
                        'status': 'error',
                        'message': 'El id del producto debe ser un valor numérico. Valor introducido: %s, en la línea %d de la orden' % (str(product_data['id']), line_count)
                    }

            if not 'quantity' in product_data:
                line_missing_args.append('quantity')
            else:
                if not isinstance(product_data['quantity'], int):
                    return {
                        'status': 'error',
                        'message': 'La cantidad del producto debe ser un valor numérico. Valor introducido: %s, en la línea %d de la orden' % (str(product_data['quantity']), line_count)
                    }

                if product_data['quantity'] > 1:
                    return {
                        'status': 'error',
                        'message': 'La cantidad del producto no debe ser mayor a 1. Valor introducido: %s, en la línea %d de la orden' % (str(product_data['quantity']), line_count)
                    }

            if not 'insole_size' in product_data:
                line_missing_args.append('insole_size')

            if line_missing_args:
                return {
                    'status': 'error',
                    'message': 'Faltan los siguientes argumentos en la línea %d de la orden: %s' % (line_count, ', '.join(line_missing_args))
                }

            product = product_product_obj.search([('id', '=', product_data['id'])])

            if not product:
                return {
                    'status': 'error',
                    'message': 'No se ha encontrado el producto con el id %d, de la línea %d de la orden' % (product_data['id'], line_count)
                }

            line_count += 1


        return {
            'status': 'success',
            'content': {
                'partner_id': customer,
                'branch_id': branch,
                'partner_invoice_id': invoice_address,
                'partner_shipping_id': delivery_address,
                'pricelist_id': pricelist,
                'payment_term_id': payment_terms,
                'x_studio_selection_field_waqzv': tipo_pedido,
                'estatus_crm': estatus_crm_record.id,
                'folio_pedido': folio_pedido,
                'is_adjustment' : ajuste or False,
                'order_line': order_line,
                'user_id': salesperson,
                'team_id': sales_team,
                'company_id': company,
                'require_signature': online_signature,
                'picking_policy': shipping_policy,
                'observations': observations
            }
        }


    def validate_update_data(self, args, sale_id):
        product_product_obj = request.env['product.product'].sudo()
        procurement_groups = request.env['procurement.group'].sudo().search([('sale_id', '=', sale_id)])
        # ordenes de fabricación que pertenecen a la orden de venta
        mrp_orders_ids = procurement_groups.stock_move_ids.created_production_id.ids
        missing_args = []
        data = {}

        estatus_crm = args.get('estatus_crm', None)
        add_materials = args.get('add_materials', None)
        is_send = args.get('is_send', None)

        #Se verifica que no puedan mandar dos acciones de estatus de CRM
        if add_materials and is_send:
            return {
                    'status': 'error',
                    'message': 'Los parametros [add_materials] y [is_send] no pueden ser ambos verdadero.'
                }
        

        # Comprueba que se hayan suplido todos los argumentos
        if not estatus_crm:
            missing_args.append('estatus_crm')
        else:
            if not isinstance(estatus_crm, int):
                return {
                    'status': 'error',
                    'message': 'El parámetro estatus_crm debe ser un valor numérico'
                }

            estatus_crm_record = request.env['crm.status'].sudo().search([('code', '=', str(estatus_crm))],limit=1)

            if not estatus_crm_record:
                return {
                    'status': 'error',
                    'message': 'No se encontró el estatus con el id %s' % estatus_crm
                }

            data.update({'estatus_crm': estatus_crm})

        if add_materials:
            mrp_orders = args.get('mrp_orders', None)

            if not mrp_orders:
                missing_args.append('mrp_orders')
            else:
                if not isinstance(mrp_orders, list):
                    return {
                        'status': 'error',
                        'message': 'El parámetro mrp_orders debe ser un array'
                    }

                data.update({'mrp_orders': mrp_orders})


        if add_materials:
            if len(mrp_orders) == 0:
                return {
                    'status': 'error',
                    'message': 'No se agregaron órdenes de fabricación'
                }

            # Comprueba que las órdenes de fabricación existan en Odoo
            for mrp_order_data in mrp_orders:
                if not mrp_order_data.get('id', None):
                    missing_args.append('mrp_orders.id')
                    break
                else:
                    if not isinstance(mrp_order_data['id'], int):
                        return {
                            'status': 'error',
                            'message': 'El id de la orden de fabricación debe ser un valor numérico. Valor introducido: %s' % str(mrp_order_data['id'])
                        }

                    if not mrp_order_data['id'] in mrp_orders_ids:
                        return {
                            'status': 'error',
                            'message': 'La orden de fabricación con id %d no pertenece a la orden de venta con id %d' % (mrp_order_data['id'], sale_id)
                        }

                    mrp_order = request.env['mrp.production'].sudo().browse(mrp_order_data['id'])

                    if mrp_order.state == 'confirmed':
                        return {
                            'status': 'error',
                            'message': 'La orden de fabricación con id %d ya fue confirmada' % (mrp_order_data['id'])
                        }

                if not mrp_order_data.get('components', None):
                    missing_args.append('mrp_orders.components')
                    break
                else:
                    if not isinstance(mrp_order_data['components'], list):
                        return {
                            'status': 'error',
                            'message': 'El parámetro mrp_orders.components debe ser un array. Valor introducido: %s' % str(mrp_order_data['components'])
                        }

                for component_data in mrp_order_data['components']:
                    if not component_data.get('id', None):
                        missing_args.append('mrp_orders.components.id')
                        break
                    else:
                        if not isinstance(component_data['id'], int):
                            return {
                                'status': 'error',
                                'message': 'El id del componente debe ser un valor numérico. Valor introducido: %s' % str(component_data['id'])
                            }

                        component = product_product_obj.sudo().search([('id', '=', component_data['id'])])

                        if not component:
                            return {
                                'status': 'error',
                                'message': 'No se ha encontrado el componente con el id %d' % component_data['id']
                            }

                    if not component_data.get('quantity', None):
                        missing_args.append('mrp_orders.components.quantity')
                        break
                    else:
                        if not isinstance(component_data['quantity'], int):
                            return {
                                'status': 'error',
                                'message': 'La cantidad del componente debe ser un valor numérico. Valor introducido: %s' % str(component_data['quantity'])
                            }

                if missing_args:
                    break


        if missing_args:
            return {
                'status': 'error',
                'message': 'Faltan los siguientes argumentos: %s' % ', '.join(missing_args)
            }
        
        #Indicadores de estatus para añadir material o modificar el envio
        data.update({'add_materials':add_materials, 'is_send': is_send})

        return {
            'status': 'success',
            'content': data
        }
