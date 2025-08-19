# -*- coding: utf-8 -*-
# from odoo import http


# class YlhcLevelMenu(http.Controller):
#     @http.route('/ylhc_level_menu/ylhc_level_menu', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ylhc_level_menu/ylhc_level_menu/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ylhc_level_menu.listing', {
#             'root': '/ylhc_level_menu/ylhc_level_menu',
#             'objects': http.request.env['ylhc_level_menu.ylhc_level_menu'].search([]),
#         })

#     @http.route('/ylhc_level_menu/ylhc_level_menu/objects/<model("ylhc_level_menu.ylhc_level_menu"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ylhc_level_menu.object', {
#             'object': obj
#         })

