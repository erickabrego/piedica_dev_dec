# -*- coding: utf-8 -*-
{
    'name': "Responsables por operación de fabricación",
    'summary': """
        Adición de responsables por operación en el centro de trabajo.
    """,
    'description': """
        Adición de usuarios responables por operación. Agregando una advertencia cuando se quiera iniciar una operación a la que no pertenecen.
    """,
    'author': "M22",
    'website': "http://m22.mx",
    'category': 'MRP',
    'version': '14.0.1',
    'depends': ['base','mrp','mrp_workorder'],
    'data': [
        'views/mrp_workcenter.xml'
    ],
    'license': 'AGPL-3'
}
