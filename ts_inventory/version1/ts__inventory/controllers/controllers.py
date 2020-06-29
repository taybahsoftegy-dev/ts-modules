# -*- coding: utf-8 -*-
# from odoo import http


# class TsInventory(http.Controller):
#     @http.route('/ts__inventory/ts__inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ts__inventory/ts__inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ts__inventory.listing', {
#             'root': '/ts__inventory/ts__inventory',
#             'objects': http.request.env['ts__inventory.ts__inventory'].search([]),
#         })

#     @http.route('/ts__inventory/ts__inventory/objects/<model("ts__inventory.ts__inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ts__inventory.object', {
#             'object': obj
#         })
