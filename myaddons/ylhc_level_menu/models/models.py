# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ylhc_level_menu(models.Model):
#     _name = 'ylhc_level_menu.ylhc_level_menu'
#     _description = 'ylhc_level_menu.ylhc_level_menu'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

