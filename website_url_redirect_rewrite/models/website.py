# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug


class Website(models.Model):
    _inherit = "website"

    def enumerate_pages(self, query_string=None):
        """Show redirected URLs in search results."""
        query = query_string or ""
        seo_redirections = list()
        redirection_records = self.env["website.seo.redirection"].search([
            "|", ("origin", "ilike", query),
            ("destination", "ilike", query),
        ])
        for record in redirection_records:
            for url in record.origin, record.destination:
                if url not in seo_redirections:
                    seo_redirections.append(url)
        # Give super() a website to work with
        # if not request.website_enabled:
        #     self.ensure_one()
        #     request.website = self
        # Yield super()'s pages
        for page in super(Website, self).enumerate_pages(query_string):
            try:
                seo_redirections.remove(page["loc"])
            except ValueError:
                pass
            yield page
        # Remove website if we were supposed to have none
        # if not request.website_enabled:
        #     request.website = None
        # Yield redirected pages not detected by super()
        for page in seo_redirections:
            yield {"loc": page}


class SeoMetadata(models.AbstractModel):
    _inherit = 'website.seo.metadata'


    def _default_website_meta(self):
        res = super(SeoMetadata,self)._default_website_meta()
        company = request.website.company_id.sudo()
        title = (request.website or company).name
        if request.website.social_default_image:
            img = request.website.image_url(request.website, 'social_default_image')
        else:
            img = request.website.image_url(company, 'logo')
        full_url = request.httprequest.full_path.partition('?')
        full_url = full_url[0]
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = self.env['website.seo.redirection'].search([("origin","=",full_url)])
        for rec in url:
            full_url = rec.destination

        default_opengraph = {
          'og:type': 'website',
          'og:title': title,
          'og:site_name': company.name,
          'og:url': base_url+full_url,
          'og:image': img,
        }
        default_twitter = {
            'twitter:card': 'summary_large_image',
            'twitter:title': title,
            'twitter:image': img + '/300x300',
        }
        return {
            'default_opengraph': default_opengraph,
            'default_twitter': default_twitter,
        }
        return res

class WebsiteInherit(models.Model):
    _inherit = "website"


    def _get_canonical_url_localized(self, lang, canonical_params):
        res = super(WebsiteInherit,self)._get_canonical_url_localized(lang, canonical_params)
        full_url = request.httprequest.full_path.partition('?')
        full_url = full_url[0]
        url = self.env['website.seo.redirection'].search([("origin","=",full_url)])
        for rec in url:
            full_url = rec.destination
        return self.get_base_url() + full_url
        return res

class ProductTemplateInherit(models.Model):
    _inherit = "product.template"


    def _compute_website_url(self):
        record = super(ProductTemplateInherit, self)._compute_website_url()
        for product in self:
            search_url = self.env['website.seo.redirection'].search([('origin','=',product.website_url)])
            if search_url.destination:
                product.website_url = search_url.destination
            else:
                if product.name:
                   product.website_url = "/shop/product/%s" % slug(product)

        return record
        