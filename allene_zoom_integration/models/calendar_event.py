import json
import requests
from odoo.exceptions import UserError
from odoo import models, fields, api
from pytz import timezone


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    is_zoom_meeting_create = fields.Boolean("Zoom Meeting")
    meeting_url = fields.Char("Meeting URL")
    meeting_id = fields.Char('Meeting ID')
    is_video_host = fields.Boolean("Video Host")
    is_video_participant = fields.Boolean("Video Participant")
    is_enable_join_before_host = fields.Boolean("Enable Join Before Host")
    is_mute_participant = fields.Boolean("Mute Participants")
    is_record_meeting_automatic_in_local = fields.Boolean("Record Meeting Automatic in Local")

    @api.model
    def create(self, vals):
        res = super(CalendarEvent, self).create(vals)
        if res.is_zoom_meeting_create:
            access_token = self.env['ir.config_parameter'].sudo().get_param('zoom_integration.access_token')
            user_res = requests.get("https://api.zoom.us/v2/users/me", headers={"authorization": "Bearer " + access_token})
            if user_res.json().get("code") and user_res.json().get("code") != 200:
                raise UserError(user_res.json().get("message"))

            user_id = user_res.json().get("id")
            meeting_url = "https://api.zoom.us/v2/users/" + user_id + "/meetings"

            start_time = res.start.astimezone(timezone(res.env.user.tz)).isoformat() if res.env.user.tz else res.start.isoformat()

            duration_min = res.duration * 60
            topic = res.name
            password = user_res.json().get("pmi")
            agenda = res.description
            type = 2
            recurrence = {}
            if res.recurrency:
                repeat_interval = res.interval
                recurrence["repeat_interval"] = repeat_interval
                if res.end_type == "forever":
                    type = 3
                else:
                    type = 8
                    if res.end_type == "end_date":
                        end_date_time = res.until.astimezone(timezone(res.env.user.tz)).isoformat() if res.env.user.tz else res.until
                        recurrence["end_date_time"] = end_date_time
                    elif res.end_type == "count":
                        end_times = res.count
                        recurrence["end_times"] = end_times
                if res.rrule_type == "daily":
                    recurrenct_type = 1
                elif res.rrule_type == "weekly":
                    recurrenct_type = 2
                    if res.su:
                        weekly_days = 1
                    elif res.mo:
                        weekly_days = 2
                    elif res.tu:
                        weekly_days = 3
                    elif res.we:
                        weekly_days = 4
                    elif res.th:
                        weekly_days = 5
                    elif res.fr:
                        weekly_days = 6
                    elif res.sa:
                        weekly_days = 7
                    recurrence["weekly_days"] = weekly_days
                elif res.rrule_type == "monthly":
                    recurrenct_type = 3
                    if res.month_by == "date":
                        monthly_day = res.day
                        recurrence["monthly_day"] = monthly_day
                    else:
                        monthly_week = res.byday
                        if res.weekday == "SU":
                            monthly_week_day = 1
                        elif res.weekday == "MO":
                            monthly_week_day = 2
                        elif res.weekday == "TU":
                            monthly_week_day = 3
                        elif res.weekday == "WE":
                            monthly_week_day = 4
                        elif res.weekday == "TH":
                            monthly_week_day = 5
                        elif res.weekday == "FR":
                            monthly_week_day = 6
                        elif res.weekday == "SA":
                            monthly_week_day = 7
                        recurrence["monthly_week"] = monthly_week
                        recurrence["monthly_week_day"] = monthly_week_day
                
                else:
                    raise UserError("Zoom does not provide the yearly Recurring meeting")
                recurrence["type"] = recurrenct_type
            settings = {
                "host_video": res.is_video_host,
                "participant_video": res.is_video_participant,
                "join_before_host": res.is_enable_join_before_host,
                "mute_upon_entry": res.is_mute_participant,
                "auto_recording": "local" if res.is_record_meeting_automatic_in_local else None
            }
            meeting_data = {
                "topic": topic,
                "type": type,
                "start_time": start_time,
                "duration": int(duration_min),
                "settings": settings,
                "password": password,
                "agenda": agenda
            }
            if type in [3, 8]:
                meeting_data["recurrence"] = recurrence
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + access_token
            }
            meeting_res = requests.post(meeting_url, data=json.dumps(meeting_data), headers=headers)
            if meeting_res.json().get("code") and meeting_res.json().get("code") != 200:
                raise UserError(meeting_res.json().get("message"))
            res.meeting_url = meeting_res.json().get("join_url")
            res.meeting_id = meeting_res.json().get('id')
            add_registrant_url = 'https://api.zoom.us/v2/meetings/' + res.meeting_id + '/registrants'
            for each in res.partner_ids:
                data = {'email': each.email,
                        'first_name': each.name}
                response = requests.post(add_registrant_url, data=json.dumps(data), headers=headers)
        return res

    def unlink(self):
        for todo in self:
            if todo.is_zoom_meeting_create:
                requests.delete('https://api.zoom.us/v2/meetings/' + todo.meeting_id)
            return super(CalendarEvent, self).unlink()

    def join_meeting(self):
        url = self.meeting_url
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }