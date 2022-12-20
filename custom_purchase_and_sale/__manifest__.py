# -*- coding: utf-8 -*-
{
    'name': "Fabricación a sucursales",
    'summary': """
        Sincronización con CRM de ventas en sucursal y fabrica.
    """,
    'description': """
        Sincronización con CRM de ventas en sucursal y fabrica.
    """,
    'author': "M22",
    'website': "http://m22.mx",
    'category': 'Venta y compra',
    'version': '14.0.1',
    'depends': ['base','sale_management','purchase','crm_sync_orders','hr','purchase_request','merge_deliveries_bs'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company.xml',
        'views/branch_factory.xml',
        'views/sale_order.xml'
    ],
    'license': 'AGPL-3'
}
