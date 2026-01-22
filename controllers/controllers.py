# -*- coding: utf-8 -*-
# from odoo import http


# class Winery(http.Controller):
#     @http.route('/winery/winery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/winery/winery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('winery.listing', {
#             'root': '/winery/winery',
#             'objects': http.request.env['winery.winery'].search([]),
#         })

#     @http.route('/winery/winery/objects/<model("winery.winery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('winery.object', {
#             'object': obj
#         })
