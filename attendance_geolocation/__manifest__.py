# -*- coding: utf-8 -*-
#################################################################################
# Author      : CodersFort (<https://codersfort.com/>)
# Copyright(c): 2017-Present CodersFort.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://codersfort.com/>
#################################################################################

{
    "name": "Attendance Geolocation (Attendance Location)",
    "summary": "Adds to Odoo standard attendance system (also KIOSKMODE) the posibility of Geolocate the employee when check-in/check-out.",
    "version": "14.0.1",
    "description": """
        This module helps you to log the employees attendance check in / check out location information and create a direct links to Google Maps.

        Attendance Geolocation.
        Attendance Location.
        HR Attendance Location.
        HR Attendance Geolocation.
        check in / check out location.
        Attendance check in / check out location.
        latitude and longitude.
        Attendance latitude and longitude.
        Attendance Google Map.
        Google Map.        
    """,    
    "author": "CodersFort",
    "maintainer": "Ananthu Krishna",
    "license" :  "Other proprietary",
    "website": "http://www.codersfort.com",
    "images": ["images/attendance_geolocation.png"],
    "category": "Employees",
    "depends": [
        "base",
        "hr_attendance",
    ],
    "data": [
        "data/location_data.xml",
        "views/assets.xml",
        "views/hr_attendance_views.xml",
    ],
    "qweb": [],
    "installable": True,
    "application": True,
    "price"                :  17,
    "currency"             :  "EUR",
    "pre_init_hook"        :  "pre_init_check",   
}
