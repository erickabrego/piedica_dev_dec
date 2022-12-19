from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MRPWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def button_start(self):
        res = super().button_start()
        for rec in self:
            if not self.env.user.id in rec.workcenter_id.x_allowed_user_ids.ids:
                raise ValidationError(f"El usuario {self.env.user.name} no está autorizado para iniciar esta operación.")
        return res

    def button_finish(self):
        for rec in self:
            if not self.env.user.id in rec.workcenter_id.x_allowed_user_ids.ids:
                raise ValidationError(f"El usuario {self.env.user.name} no está autorizado para finalizar esta operación.")
        return super().button_finish()

    def button_pending(self):
        res = super(MRPWorkorder, self).button_pending()
        for rec in self:
            if not self.env.user.id in rec.workcenter_id.x_allowed_user_ids.ids:
                raise ValidationError(f"El usuario {self.env.user.name} no está autorizado para detener esta operación.")
        return res

    def button_unblock(self):
        res = super(MRPWorkorder, self).button_unblock()
        for rec in self:
            if not self.env.user.id in rec.workcenter_id.x_allowed_user_ids.ids:
                raise ValidationError(f"El usuario {self.env.user.name} no está autorizado para desbloquear esta operación.")
        return res


