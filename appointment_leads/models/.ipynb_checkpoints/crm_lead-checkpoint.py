from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class CRMLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def create(self, vals_list):
        res = super(CRMLead, self).create(vals_list)
        try:
            res.set_marketing_fields()
        except Exception as e:
            _logger.info(e)
        return res

    def write(self, vals):
        res = super(CRMLead, self).write(vals)
        try:
            if vals.get('partner_id'):
                self.set_marketing_fields()
        except Exception as e:
            _logger.info(e)
        return res

    def set_marketing_fields(self):
        for rec in self:
            rec["campaign_id"] = rec.partner_id.x_campaign_id.id
            rec["medium_id"] = rec.partner_id.x_medium_id.id
            rec["source_id"] = rec.partner_id.x_source_id.id

    def action_schedule_meeting(self):
        res = super(CRMLead, self).action_schedule_meeting()
        res["context"].pop("default_attendee_ids")
        return res