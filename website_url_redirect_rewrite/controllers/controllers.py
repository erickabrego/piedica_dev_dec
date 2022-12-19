# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteSeoRedirection(http.Controller):
#     @http.route('/website_seo_redirection/website_seo_redirection/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_seo_redirection/website_seo_redirection/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_seo_redirection.listing', {
#             'root': '/website_seo_redirection/website_seo_redirection',
#             'objects': http.request.env['website_seo_redirection.website_seo_redirection'].search([]),
#         })

#     @http.route('/website_seo_redirection/website_seo_redirection/objects/<model("website_seo_redirection.website_seo_redirection"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_seo_redirection.object', {
#             'object': obj
#         })
