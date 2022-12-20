    # -*- coding: utf-8 -*-pack
from odoo.exceptions import ValidationError
from odoo import fields, models
import requests
import logging
_logger = logging.getLogger(__name__)

class EnviaResCompany(models.Model):
    _inherit = "res.company"

    envia_api_url = fields.Char(string="Envia API_URL", help="Enter Envia API URL", default="https://api.envia.com/")
    envia_carrier_url = fields.Char(string="Carrier API URL",default="https://queries.envia.com/")
    envia_api_key = fields.Char(string="Envia API_KEY", help="Enter Your Envia Account's API KEY, You Can Get From Setting")
    use_envia_shippiing_provider = fields.Boolean(copy=False, string="Are You Use Envia.?",
                                                        help="If use Envia shipping Integration than value set TRUE.",
                                                        default=False)


    def import_available_carrier(self):
        api_url = "{0}carrier?country_code={1}".format(self.envia_carrier_url,self.country_id.code)
        header = {"Content-Type": "application/json",
                  "Authorization": "Bearer {}".format(self.envia_api_key)}
        available_carrier_obj = self.env['available.carrier']
        try:
            response_data = requests.get(url=api_url,headers=header)
            if response_data.status_code in [200,201]:
                response_data = response_data.json()
                for carrier in response_data.get('data'):
                    carrier_name = carrier.get('name')
                    country_code = carrier.get('country_code')
                    if not available_carrier_obj.sudo().search([('carrier_name','=','{}'.format(carrier_name))]):
                        available_carrier_obj.sudo().create({'carrier_name':'{}'.format(carrier_name),
                                                             'country_code':'{}'.format(country_code)})
                    else:
                        _logger.info("carrier is already exist")
                        available_carrier_obj.sudo().write({'carrier_name': '{}'.format(carrier_name),
                                                             'country_code': '{}'.format(country_code)})
                return {
                        'effect': {
                            'fadeout': 'slow',
                            'message': "Yeah! Carriers Successfully Import.",
                            'img_url': '/web/static/src/img/smile.svg',
                            'type': 'rainbow_man',
                        }
                        }

            else:
                raise ValidationError("Get Some Error In Response {}".format(response_data.text))
        except Exception as E:
            raise ValidationError(E)

    def import_response(self):
        data =    {
                      "data": [
                        {
                          "name": "fedex",
                          "country_code": "MX"
                        },
                        {
                          "name": "dhl",
                          "country_code": "MX"
                        },
                        {
                          "name": "redpack",
                          "country_code": "MX"
                        },
                        {
                          "name": "sendex",
                          "country_code": "MX"
                        },
                        {
                          "name": "noventa9Minutos",
                          "country_code": "MX"
                        },
                        {
                          "name": "carssa",
                          "country_code": "MX"
                        },
                        {
                          "name": "ups",
                          "country_code": "MX"
                        },
                        {
                          "name": "estafeta",
                          "country_code": "MX"
                        },]}
        return data