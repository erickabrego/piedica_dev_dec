from odoo import api, fields, models

class BranchFactory(models.Model):
    _name = 'branch.factory'
    _description = 'Configuración de sucursal a fabrica'

    branch_id = fields.Many2one(comodel_name="res.company", string="Sucursal")
    factory_id = fields.Many2one(comodel_name="res.company", string="Fabrica")
    department_id = fields.Many2one(comodel_name="hr.department", string="Departamento")
    name = fields.Char(string="Nombre completo", compute="_get_rule_name")
    delivery_address = fields.Many2one(comodel_name="res.partner", string="Dirección de sucursal")

    @api.depends("branch_id","factory_id")
    def _get_rule_name(self):
        for rec in self:
            rec["name"] = f"[{rec.branch_id.name}] - [{rec.factory_id.name}]"

