{
    'name': "Oportunidades de citas en línea",
    'summary': "Oportunidades de citas en línea",
    'description': "Agrega la opción para crear oportunidades a partir de citas en línea",
    'category': 'Uncategorized',
    'version': '14.0.1',
    'depends': ['website_calendar', 'crm', 'sale_crm', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'views/calendar_appointment_views.xml',
        'views/website_calendar_templates.xml',
        'views/res_partner_simplified.xml',
        'views/calendar_event.xml',
        'wizard/default_lead_event.xml'
    ]
}
