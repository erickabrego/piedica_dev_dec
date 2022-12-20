# -*- coding: utf-8 -*-pack
from odoo import fields, api, models
from odoo.exceptions import ValidationError
import requests
import logging
import json
import base64

_logger = logging.getLogger("Envia")


class EnviaDeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(selection_add=[("envia", "Envia")], ondelete={'envia': 'set default'})
    envia_packaging_id = fields.Many2one('product.packaging', string="Envia Package", help="Default Package")
    envia_shipping_carrier = fields.Many2many('available.carrier', string="Available Carrier Service",
                                              help="available carrier")
    envia_package_type = fields.Selection(
        [('envelope', 'Envelope'), ('box', 'Box'), ('pallet_120x120', 'Pallet_120x120')], string="Envia Package Type",
        help="Choose Package Type For Your Shipmet")
    envia_weight_uom = fields.Selection([('KG', 'KG'),
                                         ('LB', 'LB')])

    def api_calling(self, api_url, request_data):
        """
        :return: this method return response
        """
        api_key = self.company_id.envia_api_key
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer {}".format(api_key)}
        try:
            response_data = requests.post(url=api_url, headers=headers, data=json.dumps(request_data))
        except Exception as error:
            raise ValidationError(error)
        if response_data.status_code in [200, 201]:
            try:
                return response_data.json()
            except Exception:
                raise ValidationError(response_data.text)
        else:
            raise ValidationError(response_data.text)

    def convert_weight(self, shipping_weight):
        grams_for_kg = 1000  # 1 Kg to Grams
        uom_id = self.env['product.template']._get_weight_uom_id_from_ir_config_parameter()
        if self.weight_uom == "GRM" and uom_id.name == 'kg':
            return round(shipping_weight * grams_for_kg, 3)
        else:
            return shipping_weight

    def parcel_data(self, pickings, order):
        """
        :param pickings:
        :return: this method return package information
        """
        envia_parcel_data = []
        # if pickings and pickings.package_level_ids_details:
        #     package_id = pickings.package_level_ids_details.package_id
        if not pickings:
            total_weight = sum(
                [(line.product_id.weight * line.product_uom_qty) for line in order.order_line if not line.is_delivery])
            bulk_weight = total_weight
        else:
            bulk_weight = pickings.weight_bulk
        if pickings:
            for package in pickings.package_ids:
                package_dict = {
                    "content": package.name or "",
                    "amount": 1,
                    "type": "{}".format(self.envia_package_type),
                    "dimensions": {
                        "length": int(package.packaging_id.packaging_length) or 0,
                        "width": int(package.packaging_id.width) or 0,
                        "height": int(package.packaging_id.height) or 0
                    },
                    "weight": int(package.shipping_weight) or 0,
                    "insurance": 0,
                    "declaredValue": 0,
                    "weightUnit": self.envia_weight_uom,
                    "lengthUnit": "CM"
                }
                envia_parcel_data.append(package_dict)
        if bulk_weight:
            pacel_data = {
                "content": self.envia_packaging_id.name or "",
                "amount": 1,
                "type": "{}".format(self.envia_package_type),
                "dimensions": {
                    "length": int(self.envia_packaging_id.packaging_length) or "",
                    "width": int(self.envia_packaging_id.width) or "",
                    "height": int(self.envia_packaging_id.height) or ""
                },
                "weight": int(bulk_weight) or "",
                "insurance": 0,
                "declaredValue": 0,
                "weightUnit": self.envia_weight_uom,
                "lengthUnit": "CM"
            }
            envia_parcel_data.append(pacel_data)
            return envia_parcel_data

    def request_data(self, order, pickings, carrier=False):
        """
        :return: this method return request data for api
        """

        # Shipper and Recipient Address
        shipper_address = self.company_id
        if order:
            receipient_address = order.partner_id
        else:
            receipient_address = pickings.partner_id
        # check sender Address
        if not shipper_address.zip or not shipper_address.city or not shipper_address.country_id or not shipper_address.email or not shipper_address.phone:
            raise ValidationError("Please define sender proper address, phone number and email")

        # check Receiver Address
        if not receipient_address.zip or not receipient_address.city or not receipient_address.country_id or not receipient_address.email or not receipient_address.phone:
            raise ValidationError("Please define receiver proper address, phone number and email")

        request_data = {
            "origin": {
                "name": "{}".format(shipper_address.name or ""),
                "company": "{}".format(shipper_address.name or ""),
                "email": "{}".format(shipper_address.email or ""),
                "phone": "{}".format(shipper_address.phone or ""),
                "street": "{}".format(shipper_address.street or ""),
                "number": "crescent ave",
                "district": "{}".format(shipper_address.city or ""),
                "city": "{}".format(shipper_address.city or ""),
                "state": "{}".format(shipper_address.state_id.code or ""),
                "country": "{}".format(shipper_address.country_id.code or ""),
                "postalCode": "{}".format(shipper_address.zip or ""),
                "reference": ""
            },
            "destination": {
                "name": "{}".format(receipient_address.name or ""),
                "company": "{}".format(receipient_address.name or ""),
                "email": "{}".format(receipient_address.email or ""),
                "phone": "{}".format(receipient_address.phone or ""),
                "street": "{}".format(receipient_address.street or ""),
                "number": "crescent ave",
                "district": "{}".format(receipient_address.city or ""),
                "city": "{}".format(receipient_address.city or ""),
                "state": "{}".format(receipient_address.state_id.code or ""),
                "country": "{}".format(receipient_address.country_id.code or ""),
                "postalCode": "{}".format(receipient_address.zip or ""),
                "reference": ""
            },
            "packages": self.parcel_data(pickings, order),
            "shipment": {
                "carrier": carrier,
                "type": 1
            }
        }
        _logger.info(request_data)
        return request_data

    def envia_rate_shipment(self, order):
        self.ensure_one()
        envia_shipping_charge_obj = self.env['envia.shipping.charge']
        order_lines_without_weight = order.order_line.filtered(
            lambda line_item: not line_item.product_id.type in ['service',
                                                                'digital'] and not line_item.product_id.weight and not line_item.is_delivery)
        for order_line in order_lines_without_weight:
            return {'success': False, 'price': 0.0,
                    'error_message': "Please define weight in product : \n %s" % (order_line.product_id.name),
                    'warning_message': False}
        receipient_address = order.partner_id
        # url = "https://api.envia.com/ship/rate/"
        # name = receipient_address.name.replace(" ","")
        # company_name = receipient_address.name.replace(" ","")
        if not receipient_address.email:
            raise ValidationError("Please Define Receiver Email")
        # email = receipient_address.email
        # carrier = self.envia_shipping_carrier.carrier_name
        existing_records = envia_shipping_charge_obj.sudo().search(
            [('sale_order_id', '=', order and order.id)], )
        existing_records.sudo().unlink()
        api_url = "%sship/rate/" % self.company_id.envia_api_url  # "https://api.envia.com/ship/rate/"
        for carrier in self.envia_shipping_carrier:
            try:
                request_data = self.request_data(order=order, pickings=False, carrier=carrier.carrier_name)

                response_data = self.api_calling(api_url, request_data)
                rate_data = response_data.get('data')
                if rate_data:

                    for shipping_charge in rate_data:
                        envia_shipping_charge_obj.sudo().create({
                            "envia_carrier": "{}".format(shipping_charge.get('carrier')),
                            "envia_service": "{}".format(shipping_charge.get('service')),
                            "envia_delivery_estimate": "{}".format(shipping_charge.get('deliveryEstimate')),
                            "envia_total_price": "{}".format(shipping_charge.get('totalPrice')),
                            "envia_currency": "{}".format(shipping_charge.get('currency')),
                            'sale_order_id': order and order.id

                        })
            except Exception as E:
                continue
        envia_charge_id = self.env['envia.shipping.charge'].sudo().search(
            [('sale_order_id', '=', order and order.id)], order='envia_total_price', limit=1)
        if not envia_charge_id:
            return {'success': False, 'price': 0.0, 'error_message': "Rate Not Found!",
                    'warning_message': False}
        order.envia_shipping_charge_id = envia_charge_id and envia_charge_id.id

        return {'success': True, 'price': envia_charge_id and envia_charge_id.envia_total_price or 0.0,
                'error_message': False, 'warning_message': False}

    @api.model
    def envia_send_shipping(self, pickings):
        shipping_data = []
        carrier =  pickings.sale_id and pickings.sale_id.envia_shipping_charge_id and pickings.sale_id.envia_shipping_charge_id.envia_carrier
        request_data = self.request_data(order=False, pickings=pickings,carrier=carrier).copy()
        request_data['shipment']['service'] = "{}".format(
            pickings.sale_id and pickings.sale_id.envia_shipping_charge_id and pickings.sale_id.envia_shipping_charge_id.envia_service)
        add_data = {"settings": {
            "printFormat": "PDF",
            "printSize": "STOCK_4X6",
            "comments": "comentarios de el envío"
        }}
        request_data = request_data.copy()
        request_data.update(add_data)
        api_url = "%sship/generate/" % self.company_id.envia_api_url
        response_data = self.api_calling(api_url, request_data)
        _logger.info(response_data)
        try:
            if response_data.get('meta') == "generate":
                tracking_num = []
                track_url = []
                for response in response_data.get('data'):
                    tracking_number = response.get('trackingNumber')
                    tracking_num.append(str(tracking_number))
                    tracking_url = response.get('trackUrl')
                    track_url.append(tracking_url)
                    label = response.get('label')
                    pickings.envia_tracking_url = ','.join(track_url)
                    pickings.envia_label = label
                    headers = {'Content-Type': "application/x-www-form-urlencoded", 'Accept': "application/pdf"}
                    pdf_response = requests.request("GET", url=label, headers=headers)
                    binary_data = base64.b64encode(pdf_response.content)
                    pickings.carrier_tracking_ref = ','.join(tracking_num)
                    logmessage = ("<b>Tracking Numbers:</b> %s") % (tracking_number)
                    pickings.message_post(body=logmessage,
                                          attachments=[("%s.pdf" % (tracking_number), pdf_response.content)])
                    shipping_data = {
                        'exact_price': float(0.0),
                        'tracking_number': ','.join(tracking_num)}
                    shipping_data = [shipping_data]
                return shipping_data
            else:
                raise ValidationError(response_data)
        except Exception as E:
            raise ValidationError(E)

    def envia_get_tracking_link(self, pickings):
        """
        :param pickings:
        :return: this method return parcel status and tracking link
        """

        return "https://envia.com/en-US/tracking?label=%s&cntry_code=us" % (pickings.carrier_tracking_ref)

    def envia_cancel_shipment(self, picking):
        api_url = "%s/ship/cancel/" % self.company_id.envia_api_url
        data = {"carrier": "{}".format(picking.sale_id.envia_shipping_charge_id.envia_carrier),
                "trackingNumber": "{}".format(picking.carrier_tracking_ref)}
        try:
            response_data = self.api_calling(api_url=api_url, request_data=data)
            if response_data.get('meta') == "cancel":
                _logger.info("Successfully Cancel")
            else:
                raise ValidationError(response_data)
        except Exception as E:
            raise ValidationError(E)
