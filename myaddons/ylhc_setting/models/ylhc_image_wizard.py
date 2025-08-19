# -*- coding: utf-8 -*-

from odoo import models, fields, api


class YlhcBkImageWizard(models.TransientModel):
    '''
    background image wizard
    '''
    _name = 'ylhc_setting.image_wizard'
    _description = 'background image wizard'

    data = fields.Binary(string='data', required=True)
    opacity = fields.Float(string='theme opacity', default=0.8)
