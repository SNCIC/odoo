# -*- coding: utf-8 -*-

from odoo import fields, models, api
import base64
from datetime import date, datetime
from odoo.tools.misc import file_path


class YlhcCompany(models.Model):
    '''
    extend to support current mode and current style
    '''
    _inherit = "res.company"

    setting_id = fields.Many2one(
        comodel_name="ylhc_setting.setting",
        ondelete="cascade",
        string="setting id")
    
    def _get_default_favicon_icon(self):
        """
        get default favicon icon form  static path
        """
        tmp_path = file_path('ylhc_setting/static/src/img/favicon.png')
        return base64.b64encode(open(tmp_path, 'rb').read())
        
    favicon_icon = fields.Binary(
        string='Web Favicon Icon', default='_get_default_favicon_icon')

    def _get_default_small_logo(self):
        '''
        get the default small logo
        :return:
        '''
        tmp_path = file_path('ylhc_setting/static/images/logo_small.png')
        return base64.b64encode(open(tmp_path, 'rb').read())

    logo_small = fields.Binary(
        default=_get_default_small_logo, 
        string="Company Small Logo",
        attachment=True,
        help="This field holds the image used as logo for the company, limited to 128x128px.")

    def get_mode_domain(self):
        """
        get mode domain dynamic
        :return:
        """
        owner = 'res.company, {company_id}'.format(
            company_id=self.env.user.company_id.id)
        return [('owner', '=', owner)]

    def get_company_mode_data(self):
        '''
        get company mode data
        :return:
        '''
        return self.get_mode_data()

    def ensure_setting_id(self):
        '''
        check setting id
        :return:
        '''
        self.ensure_one()
        if self.setting_id:
            return
        
        # get from system setting
        system_setting = self.env["ylhc_setting.setting"].search(
            [("owner", "=", False)], limit=1)
        if system_setting:
            new_setting = system_setting.copy({
                'owner': 'res.company, {company_id}'.format(company_id=self.id),
            })
            self.setting_id = new_setting
        
        return self.setting_id

    @api.model
    def get_theme_setting(self):
        '''
        get company setting
        :return:
        '''
        record = self.env.user.company_id
        record.ensure_setting_id()
        record.setting_id.ensure_current_theme_style()
        
        result = record.setting_id.read()[0]
        result["current_theme_mode"] = record.setting_id.current_theme_mode.id
        result["current_theme_style"] = record.setting_id.current_theme_style.id
        for key, item in result.items():
            if isinstance(item, datetime):
                result[key] = fields.Datetime.to_string(item)
            if isinstance(item, date):
                result[key] = fields.Date.to_string(item)

        return result

    def check_default_data(self):
        """
        check default data
        :return:
        """
        owner = 'res.company, {company_id}'.format(company_id=self.id)
        self.env["ylhc_setting.theme_mode"].check_default_mode_data(owner)

    def save_theme_setting(self, settings):
        '''
        save theme setting
        :param settings:
        :return:
        '''
        self.ensure_setting_id()
        self.setting_id.write(settings)
