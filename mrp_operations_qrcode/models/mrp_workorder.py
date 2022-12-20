from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'


    def button_start(self):
        if self.production_id:
            self.production_id.increment_operation_index()

        return super().button_start()


    def try_to_finish_from_scan(self):
        """
        Se usa principalmente para poder hacer la validación de que haya pasado
        el tiempo mínimo requerido para poder finalizar la operación mediante
        el escaneo de QR
        """

        res = self.env['mrp.workcenter.productivity'].search([('workorder_id', '=', self.id), ('date_end', '=', False)])

        if not res:
            return {
                'status': 'warning',
                'message': ('Hubo un problema con la operación <b>%s</b>' % self.name)
            }

        date_start = res[0].date_start
        diff = datetime.now() - date_start
        duration = diff.seconds
        minutes = int(duration / 60) >> 0;
        seconds = duration % 60;
        duration_float = minutes + seconds / 60;


        if duration_float < self.duration_expected:
            return {
                'status': 'warning',
                'message': ('Aun no ha pasado el tiempo mínimo para terminar la operacion <b>%s</b>' % self.name)
            }

        return self.button_finish()


    def get_states_selection(self):
        return dict(self._fields['state']._description_selection(self.env))
