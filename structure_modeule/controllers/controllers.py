# -*- coding: utf-8 -*-
from odoo import http

# class StructureModeule(http.Controller):
#     @http.route('/structure_modeule/structure_modeule/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/structure_modeule/structure_modeule/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('structure_modeule.listing', {
#             'root': '/structure_modeule/structure_modeule',
#             'objects': http.request.env['structure_modeule.structure_modeule'].search([]),
#         })

#     @http.route('/structure_modeule/structure_modeule/objects/<model("structure_modeule.structure_modeule"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('structure_modeule.object', {
#             'object': obj
#         })