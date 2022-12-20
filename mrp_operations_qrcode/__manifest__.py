{
    'name': "Operaciones de fabricación con código QR",
    'summary': "Utiliza códigos QR para el manejo de las operaciones de fabricación",
    'description': "Utiliza códigos QR para el manejo de las operaciones de fabricación",
    'category': 'Uncategorized',
    'version': '14.0.1',
    'depends': ['mrp', 'barcodes', 'portal', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/mrp_views.xml',
    ],
    'qweb': [
        'static/src/xml/operations_scan_templates.xml'
    ]
}
