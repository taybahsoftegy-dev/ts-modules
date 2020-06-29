# -*- coding: utf-8 -*-
# from odoo import http


# class TsSales(http.Controller):
#     @http.route('/ts__sales/ts__sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ts__sales/ts__sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ts__sales.listing', {
#             'root': '/ts__sales/ts__sales',
#             'objects': http.request.env['ts__sales.ts__sales'].search([]),
#         })

#     @http.route('/ts__sales/ts__sales/objects/<model("ts__sales.ts__sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ts__sales.object', {
#             'object': obj
#         })
