# -*- coding: utf-8 -*-

from odoo import models, api, _
from .ylhc_utils import sanitize_record_datas
import json


class YlhcThemeSettingManager(models.AbstractModel):
    '''
    user theme style setting
    '''
    _name = 'ylhc_setting.setting_manager'
    _description = 'theme setting manager'

    @api.model
    def get_user_setting(self, get_style=True):
        '''
        get user setting
        :return:
        '''
        rst = dict()

        # just get the setting data
        theme_setting_mode = \
            self.env["res.config.settings"].sudo().get_theme_setting_mode()

        owner = self.get_current_owner()

        # get the setting data
        if theme_setting_mode == 'system':
            theme_settings = self.env["res.config.settings"].get_theme_setting()
        elif theme_setting_mode == 'company':
            theme_settings = self.env["res.company"].get_theme_setting()
        else:
            theme_settings = self.env["res.users"].get_theme_setting()

        cur_style_id = theme_settings.get("current_theme_style", False)
        if not cur_style_id:
            theme_mode = self.env["ylhc_setting.theme_mode"].search(
                [('owner', '=', owner)], limit=1)
            if theme_mode and theme_mode.theme_styles:
                cur_style_id = theme_mode.theme_styles[0].id
                self.update_cur_style(cur_style_id)

        theme_style = self.env["ylhc_setting.theme_style"].search(
            [('id', '=', cur_style_id)])
        theme_mode = theme_style.theme_mode
        cur_mode_name = theme_mode.name

        rst['settings'] = theme_settings
        rst['cur_style_id'] = theme_style.id
        rst['cur_mode_id'] = theme_style.theme_mode.id

        # used to set the body class
        rst['cur_mode_name'] = cur_mode_name
        rst['theme_setting_mode'] = theme_setting_mode

        rst["window_default_title"] = self.env['ir.config_parameter'].sudo().get_param(
            "ylhc_setting.window_default_title", _("Odoo"))
        rst["powered_by"] = self.env['ir.config_parameter'].sudo().get_param(
            "ylhc_setting.powered_by", _("Powered by Odoo"))
        rst["icon_policy"] = self.env['ir.config_parameter'].sudo().get_param(
            "ylhc_setting.icon_policy", _("svg_icon"))
        
        # check the user is ylhc
        rst['is_admin'] = self.env.user._is_admin()
        rst['is_system'] = self.env.user._is_system()

        rst['theme_modes'] = self.get_all_mode_data(owner)

        # get the style
        if get_style and theme_style:
            rst['style_css'] = theme_style.get_style_txt()
            if not theme_style.background_image:
                rst['mode_style_css'] = theme_mode.get_mode_css()
            else:
                rst['mode_style_css'] = theme_style.get_mode_css()
        else:
            rst['style_txt'] = ""
            rst['mode_style_css'] = ""

        sanitize_record_datas(rst)
        return rst

    @api.model
    def get_font_link(self):
        """
        get font link
        :return:
        """
        theme_settings = self.get_theme_setting()
        result = ""
        if theme_settings.get('font_name', False):
            result = '/ylhc_setting/static/fonts/{font_name}/fonts.css'.format(font_name=theme_settings.get('font_name'))
        return result
    
    @api.model
    def get_theme_setting_mode(self):
        '''
        get theme setting mode
        :return:
        '''
        config = self.env['ir.config_parameter'].sudo()
        theme_setting_mode = config.get_param(
            key='ylhc_setting.theme_setting_mode', default='system')
        return theme_setting_mode

    @api.model
    def get_theme_setting(self):
        """
        get theme setting
        :return:
        """
        # just get the setting data
        theme_setting_mode = self.get_theme_setting_mode()

        if theme_setting_mode == 'system':
            theme_settings = self.env["res.config.settings"].get_theme_setting()
        elif theme_setting_mode == 'company':
            theme_settings = self.env["res.company"].get_theme_setting()
        else:
            theme_settings = self.env["res.users"].get_theme_setting()

        return theme_settings

    @api.model
    def get_font_name(self):
        """
        get font name
        """
        theme_settings = self.get_theme_setting()
        return theme_settings.get('font_name')

    @api.model
    def update_cur_style(self, style_id):
        '''
        update user cur mode
        :return:
        '''
        setting_mode = self.env["res.config.settings"].get_theme_setting_mode()
        if setting_mode == "system":
            setting_id = self.env["ylhc_setting.setting"].search(
                [("owner", "=", False)], limit=1)
            setting_id.current_theme_style = style_id
        elif setting_mode == "company":
            company = self.env.user.company_id
            company.setting_id.current_theme_style = style_id
        elif setting_mode == "user":
            user_id = self.env.user.id
            user = self.env["res.users"].browse(user_id)
            user.setting_id.current_theme_style = style_id
        else:
            assert False

    @api.model
    def save_style_data(self, style_id, theme_style):
        '''
        save style datas
        :param style_id:
        :param style_data:
        :param owner:
        :return:
        '''
        record = self.env["ylhc_setting.theme_style"].browse(style_id)
        record.ensure_one()
        record.style_config = json.dumps(theme_style.get('style_config'))
        self.update_cur_style(style_id)

    def get_current_owner(self):
        """
        get current owner
        :return:
        """
        theme_setting_mode = \
            self.env["res.config.settings"].sudo().get_theme_setting_mode()

        # check mode data
        owner = False
        if theme_setting_mode == 'system':
            owner = False
        elif theme_setting_mode == 'company':
            owner = 'res.company, {company_id}'.format(
                company_id=self.env.user.company_id.id)
        elif theme_setting_mode == 'user':
            owner = 'res.users, {user_id}'.format(user_id=self.env.user.id)

        return owner

    # @tools.ormcache('owner')
    @api.model
    def get_all_mode_data(self, owner):
        """
        get all mode data
        """
        all_modes = self.env["ylhc_setting.theme_mode"].search([('owner', '=', owner)])
        result = []
        for mode in all_modes:
            result.append(mode.get_mode_data())
        return result

    @api.model
    def save_settings(self, settings):
        """
        save the settings
        """
        # get the setting mode
        setting_mode = self.env["res.config.settings"].get_theme_setting_mode()
        if setting_mode == "system":
            self.env["res.config.settings"].save_theme_setting(settings)
        elif setting_mode == "company":
            self.env["res.company"].save_theme_setting(settings)
        elif setting_mode == "user":
            self.env["res.users"].save_theme_setting(settings)
        else:
            assert False

        return self.get_theme_setting()
