# -*- coding: utf-8 -*-
# from odoo import http


# class TsEmployees(http.Controller):
#     @http.route('/ts__employees/ts__employees/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ts__employees/ts__employees/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ts__employees.listing', {
#             'root': '/ts__employees/ts__employees',
#             'objects': http.request.env['ts__employees.ts__employees'].search([]),
#         })

#     @http.route('/ts__employees/ts__employees/objects/<model("ts__employees.ts__employees"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ts__employees.object', {
#             'object': obj
#         })
