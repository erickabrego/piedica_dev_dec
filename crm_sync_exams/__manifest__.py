{
    'name': "Sincronización de estudios con CRM Piédica.",
    'summary': "Sincronización de los estudios de pacientes de CRM con Odoo",
    'description': "",
    'category': 'Uncategorized',
    'version': '14.0.1',
    'depends': ['base', 'mail', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'data/exam_status_data.xml',
        'views/portal_templates.xml',
        'views/res_partner_views.xml'
    ]
}
