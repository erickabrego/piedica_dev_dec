# -*- coding: utf-8 -*-
{
    'name': "Sale report",

    'summary': """
        Sale report for Piedica
        """,

    'description': """
        Sale report for Piedica
    """,
    'maintainer': 'Ateneolab Ltda',
    'website': 'https://www.ateneolab.com',
    'author': 'Ateneolab Ltda',
    'category': 'Sale',
    'version': '1.0',
    'depends': ['sale', 'bi_convert_purchase_from_sales'],
    'data': ['wizard/sale_report_wizard.xml',
             'security/ir.model.access.csv'],

}
