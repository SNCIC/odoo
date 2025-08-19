# -*- coding: utf-8 -*-

from odoo import api, fields, models


class YlhcUserSetting(models.TransientModel):
    '''
    ylhc user setting
    '''
    _inherit = 'res.config.settings'

    theme_setting_mode = fields.Selection(
        string="theme style mode",
        config_parameter="ylhc_setting.theme_setting_mode",
        selection=[('system', 'system'),
                   ('company', 'company'),
                   ('user', 'user')],
        default='system')
    
    icon_policy = fields.Selection(
        string="Menu Icon Policy",
        config_parameter="ylhc_setting.icon_policy",
        selection=[
            ('web_icon', 'web_icon'),
            ('svg_icon', 'svg_icon')],
        default='svg_icon')

    allow_debug = fields.Boolean(
        string="allow debug", 
        config_parameter="ylhc_setting.allow_debug",
        default=False)

    window_default_title = fields.Char(
        string="login title", 
        config_parameter="ylhc_setting.window_default_title",
        default="Odoo")

    powered_by = fields.Char(
        string="powered by", 
        config_parameter="ylhc_setting.powered_by",
        default="Odoo")

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

    def set_values_company_favicon(self):
        '''
        set the favicon of company
        :return:
        '''
        company = self.sudo().env['res.company']
        records = company.search([])

        if len(records) > 0:
            for record in records:
                record.write({'favicon': self._set_web_favicon(original=True)})

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.model
    def get_login_style(self):
        '''
        get login style
        :return:
        '''
        ir_config = self.env['ir.config_parameter'].sudo()
        login_style = ir_config.get_param(
            key='ylhc_setting.login_style', default='login_style1')
        return login_style

    def get_setting_record(self):
        '''
        get setting record
        :return:
        '''
        record = self.env['ylhc_setting.setting'].search([('owner', '=', False)], limit=1)
        if not record:
            record = self.env['ylhc_setting.setting'].create({'owner': False})
        return record

    @api.model
    def save_theme_setting(self, settings):
        """
        save settings
        """
        record = self.get_setting_record()
        record.write(settings)

    @api.model
    def get_theme_setting(self):
        """
        get theme settings
        """
        record = self.get_setting_record()
        record.ensure_current_theme_style()
        result = record.read()[0]

        result["current_theme_style"] = record.current_theme_style.id
        result["current_theme_mode"] = record.current_theme_style.theme_mode.id

        return result
