import werkzeug
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp

UNIT = dp.get_precision("Location")

def urlplus(url, params):
    return werkzeug.Href(url)(params or None)

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    check_in_latitude = fields.Float(
        "Check-in Latitude",
        digits=UNIT,
        readonly=True
    )
    check_in_longitude = fields.Float(
        "Check-in Longitude",
        digits=UNIT,
        readonly=True
    )
    check_out_latitude = fields.Float(
        "Check-out Latitude",
        digits=UNIT,
        readonly=True
    )
    check_out_longitude = fields.Float(
        "Check-out Longitude",
        digits=UNIT,
        readonly=True
    )
    check_in_map_link = fields.Char('Check In Map', 
        compute='_compute_check_in_map_url'
    )
    check_out_map_link = fields.Char('Check Out Map', 
        compute='_compute_check_out_map_url'
    )

    @api.depends('check_in_latitude','check_in_longitude')
    def _compute_check_in_map_url(self):
        for record in self:
            params = {
                'q': '%s,%s' % (record.check_in_latitude or '',record.check_in_longitude or ''),
                'z': 10,
            }
            record.check_in_map_link =  urlplus('https://maps.google.com/maps', params)

    @api.depends('check_out_latitude','check_out_longitude')
    def _compute_check_out_map_url(self):
        for record in self:
            params = {
                'q': '%s,%s' % (record.check_out_latitude or '',record.check_out_longitude or ''),
                'z': 10,
            }
            record.check_out_map_link = urlplus('https://maps.google.com/maps', params)
