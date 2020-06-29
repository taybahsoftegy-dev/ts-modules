# -*- coding: utf-8 -*-
# from odoo import http


# class TsPurchase(http.Controller):
#     @http.route('/ts__purchase/ts__purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ts__purchase/ts__purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ts__purchase.listing', {
#             'root': '/ts__purchase/ts__purchase',
#             'objects': http.request.env['ts__purchase.ts__purchase'].search([]),
#         })

#     @http.route('/ts__purchase/ts__purchase/objects/<model("ts__purchase.ts__purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ts__purchase.object', {
#             'object': obj
#         })
