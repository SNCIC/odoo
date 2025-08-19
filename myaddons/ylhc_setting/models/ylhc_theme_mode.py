# -*- coding: utf-8 -*-

from odoo import models, fields


class YlhcThemeMode(models.Model):
    '''
    user theme style setting
    '''
    _name = 'ylhc_setting.theme_mode'
    _description = 'ylhc theme mode'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Mode Sequence", default=0)
    is_default = fields.Boolean(string="Default")
    active = fields.Boolean(string="Active", default=True)

    setting_id = fields.Many2one(
        comodel_name="ylhc_setting.setting",
        ondelete="cascade",
        string="setting id")

    theme_styles = fields.One2many(
        string="Theme Styles",
        comodel_name="ylhc_setting.theme_style",
        inverse_name="theme_mode")

    # if owner is False, so the style own to global
    owner = fields.Reference(
        string="Owner",
        selection=[('res.company', 'res.company'),
                   ('res.users', 'res.users')],
        default=False,
        help="owner which this theme is create by, if it is false, it mean it is owned to the system!")
    
    mode_css = fields.Text(string="Mode Style Css")

    def get_mode_data(self):
        '''
        get the mode data
        :return:
        '''
        self.ensure_one()
        mode_data = self.read()[0]
        mode_data['theme_styles'] = self.theme_styles.get_styles()
        return mode_data

    def get_mode_css(self):
        """
        get mode style css
        """
        self.ensure_one()
        return self.mode_css
