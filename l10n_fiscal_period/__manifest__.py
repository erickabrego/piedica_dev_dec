# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Fiscal period",
    "version": "14.0.1.0.0",
    "category": "Accounting",
    "author": "Osmar Leyet<leyetfz@gmail.com>",
    "website": "https://www.ateneolab.com",
    "license": "AGPL-3",
    "depends": ["base", "account"],
    "data": [
        "security/fiscal_period_security.xml",
        "security/ir.model.access.csv",
        "views/period_accounting_view.xml",
    ],
}
