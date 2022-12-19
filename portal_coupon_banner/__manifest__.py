{
    'name': "Banner con cupón de descuento en portal",
    'summary': "Banner con cupón de descuento en portal",
    'description': """
        Agrega un banner en la página de portal del cliente cuando éste tiene un
        cupón de descuento disponible.
    """,
    'category': 'Uncategorized',
    'version': '14.0.1',
    'depends': ['portal', 'website_sale', 'sale_coupon'],
    'data': [
        'views/assets.xml',
        'views/coupon_views.xml',
        'views/portal_templates.xml'
    ]
}
