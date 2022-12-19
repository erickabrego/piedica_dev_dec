# -*- coding: utf-8 -*-
{
    'name': "Conciliación - Extensión Piédica ",

    'summary': """
       Conciliación-Extensión Piédica
        """,

    'description': """
        Conciliación-Extensión Piédica
    """,
    'maintainer': 'Ateneolab Ltda',
    'website': 'https://www.ateneolab.com',
    'author': 'Ateneolab Ltda',
    'category': 'Account',
    'version': '1.0',
    'depends': ['account'],
    'data': [
        'security/reconcile_security.xml',
        'security/ir.model.access.csv',
        'views/reconcile_views.xml'
    ]

}
