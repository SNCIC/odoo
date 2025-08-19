# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime
from datetime import date, datetime


class YlhcThemeUsers(models.Model):
    '''
    user theme style setting
    '''
    _inherit = "res.users"
    _description = 'user setting'

    setting_id = fields.Many2one(
        comodel_name="ylhc_setting.setting",
        ondelete="cascade",
        string="settings")

    @api.model
    def save_theme_setting(self, settings):
        '''
        save settings, create if there is no user info
        just use full when the mode is user wide mode
        :param settings:
        :return:
        '''
        self.ensure_setting_id()
        self.setting_id.write(settings)

    def ensure_setting_id(self):
        '''
        check setting id
        :return:
        '''
        self.ensure_one()
        if self.setting_id:
            return
        
        system_setting = self.env["ylhc_setting.setting"].search(
            [("owner", "=", False)], limit=1)
        if system_setting:
            new_setting = system_setting.copy({
                'owner': 'res.users, {user_id}'.format(user_id=self.id),
            })
            self.setting_id = new_setting
        
        return self.setting_id
    
    def get_theme_setting(self):
        '''
        get settings
        :return:
        '''
        record = self.env.user
        record.ensure_setting_id()
        record.setting_id.ensure_current_theme_style()
        field_names = [name for name, field in record.setting_id._fields.items() if name not in [
                "icon128x128", "icon144x144", "icon152x152", "icon192x192", "icon256x256", "icon512x512"]]
        result = record.setting_id.read(fields=field_names)[0]
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
        # check mode data
        owner = 'res.users, {user_id}'.format(user_id=self.id)
        self.env["ylhc_setting.theme_mode"].check_default_mode_data(owner)

    @api.model
    def get_user_xml_groups(self):
        '''
        :return:
        '''
        group_ids = self.env.user.groups_id.ids
        records = self.env['ir.model.data']\
            .sudo() \
            .search_read([('model', '=', 'res.groups'),
                          ('res_id', 'in', group_ids)], fields=["complete_name"])
        return {record["complete_name"]: True for record in records}

    def get_mode_domain(self):
        """
        get mode domain dynamic
        :return:
        """
        owner = 'res.users, {user_id}'.format(user_id=self.id)
        return [('owner', '=', owner)]

    @api.model
    def get_group_infos(self):
        '''
        :return:
        '''
        group_ids = self.env.user.groups_id.ids
        records = self.env['ir.model.data']\
            .sudo() \
            .search_read(
            [('model', '=', 'res.groups'),
             ('res_id', 'in', group_ids)],
            fields=["complete_name"])
        groups = {record["complete_name"]: True for record in records}

        return {
            "groups": groups,
            "group_ids": group_ids,
            "user_id": self.env.user.id
        }
