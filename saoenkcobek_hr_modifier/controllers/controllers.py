# -*- coding: utf-8 -*-
# from odoo import http


# class Saoenkcobek(http.Controller):
#     @http.route('/saoenkcobek/saoenkcobek/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/saoenkcobek/saoenkcobek/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('saoenkcobek.listing', {
#             'root': '/saoenkcobek/saoenkcobek',
#             'objects': http.request.env['saoenkcobek.saoenkcobek'].search([]),
#         })

#     @http.route('/saoenkcobek/saoenkcobek/objects/<model("saoenkcobek.saoenkcobek"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('saoenkcobek.object', {
#             'object': obj
#         })
