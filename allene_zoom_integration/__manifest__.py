# See LICENSE file for full copyright and licensing details.

{
    # Module Info.
    "name": "Zoom Meeting Integration",
    "version": "13.0.1.0.0",
    "sequence": 1,
    "category": "General",
    "license": 'LGPL-3',
    "summary": """From these module you can able to create a meeting from odoo as well as that meeting can be linked with Zoom.""",
    "description": """From these module you can able to create a meeting from odoo as well as that meeting can be linked with Zoom.""",

    # Author
    "author": "Allene Software",
    'website': 'https://www.fiverr.com/hardikgajera82?up_rollout=true',

    # Dependencies
    "depends": ['base', 'calendar'],

    # Data
    "data": [
        'views/template.xml',
        'views/res_config_settings_view.xml',
        'views/calendar_event_view.xml'
    ],

    # Odoo App Store Specific
    'images': ['static/description/zoom.png'],

    # Technical
    "application": True,
    "installable": True,
    'price': 80,
    'currency': 'EUR',
}
