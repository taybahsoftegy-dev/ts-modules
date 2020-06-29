# -*- coding: utf-8 -*-
# from odoo import http


# class TsDevelopment(http.Controller):
#     @http.route('/ts__development/ts__development/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ts__development/ts__development/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ts__development.listing', {
#             'root': '/ts__development/ts__development',
#             'objects': http.request.env['ts__development.ts__development'].search([]),
#         })

#     @http.route('/ts__development/ts__development/objects/<model("ts__development.ts__development"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ts__development.object', {
#             'object': obj
#         })
