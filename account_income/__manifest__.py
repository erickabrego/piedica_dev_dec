# -*- coding: utf-8 -*-
#############################################################################
#
#    Ateneolab Ltda
#    2021 Ateneolab Ltda(<https://www.ateneolab.com>).
#    Author: Osmar Leyet (leyetfz@gmail.com)
#
#############################################################################
{
    'name': 'Income account',
    'version': '14.0.0.1',
    'category': 'Accounting',
    'summary': 'Customized Income',
    'author': 'Ateneolab Ltda',
    'company': 'Ateneolab Ltda',
    'maintainer': 'Ateneolab Ltda',
    'website': 'https://www.ateneolab.com',
    'depends': ['account_accountant'],
    'data': [
             'security/income_security.xml',
             'security/ir.model.access.csv',
             'views/view.xml',
             'data/sequence_data.xml',
            ],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,

}
