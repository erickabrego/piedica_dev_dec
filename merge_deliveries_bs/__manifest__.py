{
    'name': "Merge transfers",
    'description': """         
     Merge multiple deliveries of a partner to create a single transfer""",
    'category': 'Operations/Inventory/Delivery',
    'application': True,
    'depends': ['stock', 'delivery'],
    'data': [
   	'security/security.xml',
        'security/ir.model.access.csv',
        'data/merge_action_data.xml',
        'views/stock_picking_inherit.xml',
        'wizard/merge_deliveries_wizard.xml'
    ],
    'images': ['static/description/banner.gif'],
    'author': "Brain Station 23 LTD",
    'website': "http://www.brainstation-23.com",
    'license': 'OPL-1',
    'version': '14.0',
    'application': True,
    'installable': True,
    'currency': 'USD',
}
