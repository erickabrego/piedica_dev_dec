# -*- coding: utf-8 -*-
{
    'name': "Website URL Redirect URL Rewrite, Bulk URL Redirect setup",
    'summary': "SEO URL Redirect, URL Rewrite for 301, 404, Bulk URL Redirect, Website URL Redirect Multiple Website URL Redirection, blog url Rewrite shop url Rewrite",
    'description': "SEO URL Redirect, URL Rewrite for 301, 404, Bulk URL Redirect, Multiple Website URL Redirection in odoo 15,14, 13, 12, 11",
    'category': 'Website',
    'version': '14.0.0.0.1',

    'depends': ['base', 'website','product','website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/seo_data.xml',
        'views/product_inherit.xml',
        'views/website_seo_redirection_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
        'demo/assets_demo.xml',
        'demo/website_seo_redirection_demo.xml',
    ],
    'price': 42,
    'currency': 'USD',
    'support': ': business@aagaminfotech.com',
    'author': 'Aagam Infotech',
    'website': 'http://aagaminfotech.com',
    'installable': True,
    'license': 'OPL-1',
    'external_dependencies': {'python': ['qrcode', 'pyotp']},
    'images': ['static/description/images/Banner-Img.png'],
}
