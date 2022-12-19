# -*- coding: utf-8 -*-
{
    'name': "Chat Irina",
    'summary': """
        Comunicación con el chat de Irina para mantener al paciente informado sobre su cita.
    """,
    'description': """
        Comunicación con el chat de Irina para mantener al paciente informado sobre su cita con diferentes condiciones para
        los mensajes.
    """,
    'author': "M22",
    'website': "https://m22.mx",
    'category': 'Productivity/Calendar',
    'version': '15.0.1',
    'depends': ['base','calendar','website_calendar','custom_purchase_and_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/ir_config_parameter.xml'
    ],
    'license': 'AGPL-3'
}
