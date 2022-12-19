# -*- coding: utf-8 -*-pack
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{

    # App information
    'name': 'Envia Shipping Integration',
    'category': 'Website',
    'version': '14.0.28.04.22',
    'summary': '',
    'license': 'OPL-1',
    'description': """Integrate & Manage Envia shipping operations from Odoo by using Odoo Envia Integration.Using Envia Integration we Export the Order to Envia and generate the label in odoo.We are providing following modules odoo shipping integration,Bluedart, Shiprocket, clickpost..""",
    # Dependencies
    'depends': ['delivery'],

    # Views
        'data': [

        'views/res_company.xml',
        'security/ir.model.access.csv',
        'views/delivery_carrier.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',

    ],

    # Odoo Store Specific
    'images': ['static/description/cover.jpg'],

    # Author
    'author': 'Vraja Technologies',
    'website': 'https://www.vrajatechnologies.com',
    'maintainer': 'Vraja Technologies',

    # Technical
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'live_test_url': 'https://www.vrajatechnologies.com/contactus',
    'price': '149',
    'currency': 'EUR',

}
# version changelog
# 14.0.12.10.21 initial version 
# 14.0.28.04.22 add feature for select multiple carrier in delivery method
