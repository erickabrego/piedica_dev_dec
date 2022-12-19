# -*- coding: utf-8 -*-
{
    'name': 'Import Employee Quotas',
    'description': """
      Import Employee Quotas
    """,
    'version': '1.0',
    'category': 'account',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'views/payment_quota_employee_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/importar_payment_quota_employee.xml',
        'views/menuitem_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
