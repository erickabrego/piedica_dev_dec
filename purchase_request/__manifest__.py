# -*- coding: utf-8 -*-
# © <2021> <ATENEOLAB>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Extensión del módulo de compras",
    'version': '14.1.0.0',
    "author": "Osmar Leyet <leyetfz@gmail.com>",
    "website": "www.ateneolab.com",
    "category": "purchase",
    "complexity": "normal",
    "description": """ Extensión del módulo de compras """,
    "depends": [
        "purchase",
        "hr",
        "purchase_requisition"
    ],
    "data": [
        "security/purchase_ext_security.xml",
        "security/ir.model.access.csv",
        "data/request_order_data.xml",
        "views/purchase_views.xml",
    ],
    "installable": True,
    "application": False,
}
