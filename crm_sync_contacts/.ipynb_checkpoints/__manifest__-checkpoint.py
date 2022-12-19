# -*- coding: utf-8 -*-
{
    'name': "crm_sync_contacts",
    'summary': """
        Sincronización de contactos de Odoo -> CRM.
    """,
    'description': """
        Sincronización de los contactos de Odoo hacia CRM con la finalidad de tener una relación entre los dos sistemas.
    """,
    'author': "M22",
    'category': 'Contacts',
    'version': '15.0.1',
    'depends': ['base','crm_sync_orders'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'wizard/res_partner_crm_sync.xml',
        "views/sale_order.xml",
        "wizard/sale_order_crm_sync.xml"
    ],
    'license': 'AGPL-3'
}
