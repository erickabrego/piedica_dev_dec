# -*- coding: utf-8 -*-
{
    'name': "Reglas de acceso a CRM",
    'summary': """
        Reglas de configuración para acceso a CRM por medio de compañías y equipos de venta.
    """,
    'description': """
        Reglas de configuración para acceso a CRM por medio de compañías y equipos de venta.
    """,
    'author': "M22",
    'website': "http://m22.mx",
    'category': 'CRM',
    'version': '14.0.1',
    'depends': ['base','crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_access_rule.xml',
        'views/res_users.xml','views/crm_team.xml'
    ],
    'license': 'AGPL-3'
}
