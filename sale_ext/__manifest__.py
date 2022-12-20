# -*- coding: utf-8 -*-
{
    'name': "sale_ext",

    'summary': """
        Addon by ext sale for piedica
        """,

    'description': """
        Addon by ext sale for piedica
    """,
    'maintainer': 'Ateneolab Ltda',
    'website': 'https://www.ateneolab.com',
    'author': 'Ateneolab Ltda',
    'category': 'Sale',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        'views/views.xml',
    ],

}
