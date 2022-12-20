# -*- coding: utf-8 -*-
#############################################################################
#
#    Ateneolab Ltda
#    2021 Ateneolab Ltda(<https://www.ateneolab.com>).
#    Author: Yen Martinez (yenykm@gmail.com)
#
#############################################################################
{
    'name': 'Customized Expenses by Piedica Group',
    'version': '14.0.3.2',
    'category': 'Accounting',
    'summary': 'Customized Expenses',
    'author': 'Ateneolab Ltda',
    'company': 'Ateneolab Ltda',
    'maintainer': 'Ateneolab Ltda',
    'website': 'https://www.ateneolab.com',
    'depends': ['account_accountant', 'hr'],
    'data': [
             'security/expenses_security.xml',
             'security/ir.model.access.csv',
             'views/expense_view.xml',
             'views/res_config_view.xml',
             'data/sequence_data.xml',
            ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,

}
