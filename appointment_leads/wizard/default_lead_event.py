from odoo import api, fields, models

class DefaultLeadEvent(models.TransientModel):
    _name = 'default.lead.event'
    _description = 'Oportunidad por defecto en evento'

    def get_default_satge(self):
        stage_id = self.env["crm.stage"].sudo().search([("name","=","Agenda cita")],limit=1)
        return stage_id.id if stage_id else False

    def get_default_opportunity(self):
        partner = self.env.context.get("default_partner_id")
        opportunity_id = self.env["crm.lead"].sudo().search([('partner_id.id','=',partner),"|",("stage_id","=",False),('stage_id.name','!=','Agenda cita')],limit=1)
        return opportunity_id.id if opportunity_id else False

    partner_id = fields.Many2one(comodel_name="res.partner", string="Paciente")
    opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Oportunidad", default=get_default_opportunity)
    event_id = fields.Many2one(comodel_name="calendar.event", string="Evento")
    name = fields.Char(string="Nombre", related="event_id.name")
    stage_id = fields.Many2one(comodel_name="crm.stage", string="Etapa", default=get_default_satge)

    def assign_lead(self):
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ("Alerta de oportunidad"),
                'message': "No existe oportunidad que asignar.",
                'type': 'warning',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
        if not self.opportunity_id:
            return notification
        self.event_id.opportunity_id = self.opportunity_id.id
        self.event_id.opportunity_id.x_calendar_event = self.event_id.id
        notification["params"]["message"] = "La asignación de la oportunidad fue correcta y se cambio de etapa."
        notification["params"]["type"] = "success"
        self.opportunity_id.stage_id = self.stage_id.id
        return notification



