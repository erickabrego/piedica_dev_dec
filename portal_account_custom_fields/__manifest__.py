{
    'name': "Campos custom en cuenta de usuario en el portal",
    'summary': "Campos custom en perfil en portal",
    'description': "Agrega campos custom en la cuenta de usuario en el portal del sitio web",
    'category': 'Uncategorized',
    'version': '14.0.1',
    'depends': ['base', 'portal'], #'web', 'web_editor'
    'data': [
        'security/ir.model.access.csv',
        # 'views/assets.xml',
        'views/res_partner_views.xml',
        'views/portal_templates.xml',
        'data/molestias.xml'
    ]
}
