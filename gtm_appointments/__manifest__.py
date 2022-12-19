{
    'name': "Google Tag Manager - Citas",
    'summary': "Integra Google Tag Manager en Odoo para registrar citas",
    'description': """
        Integra Google Tag Manager en Odoo para registrar citas
    """,
    'category': '',
    'version': '14.0.1',
    'depends': ['web', 'website', 'website_calendar'],
    'data': [
        'views/assets.xml',
        'views/res_config_settings_views.xml',
        'views/website_templates.xml'
    ]
}
