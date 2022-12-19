# -*- coding: utf-8 -*-
from odoo import api, models,fields,_
from odoo.http import local_redirect, request
from odoo.addons.http_routing.models.ir_http import slug



class ProductTemplate(models.Model):
    _inherit = "product.template"


    url_key = fields.Char(string="Destination",help="Source for product")
    url_key2 = fields.Char(string="Source",help="Destination for product")


    @api.onchange('url_key')
    def _onchange_seo_product(self):
      vals = {     
         'destination' : self.url_key,
         'origin' :self.url_key2,
        }
      seo_destination_key = self.env['website.seo.redirection'].create(vals)


    def seo_redirect_url_product(self):
      active_ids = self.env.context.get('active_ids')
      count = len(active_ids)
      rec = self.env['product.template'].browse(active_ids)
      for order in rec:
        get_value = order.url_key

        
      return {
        'name': _('Message'),
        'view_type': 'form',
        "view_mode": 'form',
        'res_model': 'open.wizard_product',
        'type': 'ir.actions.act_window',
        'target': 'new',
        'context': {'default_example_count': count},
        }


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"


    url_key = fields.Char(string="Destination",help="Source for category")
    url_key2 = fields.Char(string="Source",help="Destination for category")



    @api.onchange('url_key')
    def _onchange_seo_category(self):
      vals = {     
         'origin' :self.url_key2,
         'destination' : self.url_key,
        }
      seo_destination = self.env['website.seo.redirection'].create(vals)


    def seo_redirect_url_category(self):
        active_ids = self.env.context.get('active_ids')
        count = len(active_ids)
        order_id = self.env['open.wizard_category'].browse(active_ids)
        
        
        return {
          'name': _('Message'),
          'view_type': 'form',
          "view_mode": 'form',
          'res_model': 'open.wizard_category',
          'type': 'ir.actions.act_window',
          'target': 'new',
          'context': {'default_example_count': count},
          }




class openwizardproduct(models.TransientModel):
    _name = "open.wizard_product"
    _description = "Wizard Product"

    example_count = fields.Integer("Count",readonly="1")


class openwizard(models.TransientModel):
    _name = "open.wizard_category"
    _description = "Wizard Category"

    example_count = fields.Integer("Count",readonly="1")





