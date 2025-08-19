# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, tools
import json


class YlhcThemeStyle(models.Model):
    '''
    Theme style
    '''
    _name = 'ylhc_setting.theme_style'
    _description = 'awesome theme style'
    _order = 'sequence asc, id asc'

    name = fields.Char(string="style name", required=True)
    theme_mode = fields.Many2one(
        comodel_name="ylhc_setting.theme_mode",
        string="theme mode",
        ondelete="cascade")
    
    mode_css = fields.Text(string="mode style scss", related="theme_mode.mode_css")
    style_css = fields.Text(string="style css")

    is_default = fields.Boolean(string="is default", default=True)

    background_image = fields.Binary(string="background image")
    opacity = fields.Float(string="opacity", default=1.0)

    owner = fields.Reference(
        string="owner",
        related="theme_mode.owner",
        help="Owner which this theme is create by")

    sequence = fields.Integer(string="style sequence", default=0)
    style_config = fields.Text(string="style config")

    def get_style(self):
        '''
        get simple style data
        :return:
        '''
        self.ensure_one()
        style_config = json.loads(self.style_config or '{}')
        style_vars = style_config.get("variables", [])
        identities = style_config.get("identities", {})
        if not identities:
            for theme_var in style_vars:
                if theme_var.get("identity", False):
                    identities[theme_var["identity"]] = theme_var.get("value", "")
            style_config["identities"] = identities

        result = {
            "id": self.id,
            "name": self.name,
            "is_default": self.is_default,
            "sequence": self.sequence,
            "style_config": style_config,
            "mode_css": self.mode_css,
            "style_css": self.style_css,
            "css": self.get_style_txt(style_vars),
        }

        return result

    def is_semi_transparent(self):
        '''
        is semi transparent
        :return:
        '''
        self.ensure_one()
        return self.opacity < 1.0

    def get_mode_css(self):
        '''
        get mode styles
        :return:
        '''
        self.ensure_one()
        return self.theme_mode.get_mode_css()

    def set_bk_image(self, wizard_id):
        """
        set background image
        """
        self.ensure_one()
        wizard = self.env["ylhc_setting.image_wizard"].browse(
            wizard_id)

        self.background_image = wizard.data
        self.opacity = wizard.opacity
        
        # reutrn the image url
        url = self.get_background_image_url()
    
        # clear cache
        self.clear_caches()

        return url
    
    def get_background_image_url(self):
        """
        get image url
        """
        self.ensure_one()
        if self.background_image:
            return 'web/image/ylhc_setting.theme_style/' + str(self.id) + '/background_image'
        else:
            return False

    def get_style_txt(self, style_vars=None):
        '''
        get style txt
        :return:
        '''
        self.ensure_one()

        # get all the vars
        if not style_vars:
            style_config = json.loads(self.style_config or '{}')
            style_vars = style_config.get("variables", [])

        style_css = "\n\r:root {"
        for theme_var in style_vars:
            var_name = theme_var.get("name", "")
            if not var_name.startswith('--'):
                style_css += '\n' + f'--{var_name}: {theme_var.get("value", "")};'
            else:
                style_css += '\n' + f'{var_name}: {theme_var.get("value", "")};'
        style_css += "\n\r}"
        # add the mode css
        style_css += '\n' + self.mode_css if self.mode_css else ''
        # add the style css
        style_css += '\n' + self.style_css if self.style_css else ''
        return style_css

    def get_styles(self):
        '''
        get styles
        :return:
        '''
        rst = []
        for record in self:
            rst.append(record.get_style())
        return rst
    
    @api.model
    def clone_style(self, style_id):
        """
        clone style
        """
        theme_style = self.browse(style_id)
        if not theme_style:
            theme_mode = self.env["ylhc_setting.theme_mode"].search([('owner', '=', False)], limit=1)
            if not theme_mode:
                return False
            theme_styles = theme_mode.theme_styles
            if not theme_styles:
                return False
            theme_style = theme_styles[0]

        owner = self.env['ylhc_setting.setting_manager'].get_current_owner()
        new_style = theme_style.copy({
            'name': self.name or '' + ' clone',
            'owner': owner,
            'is_default': False,
            'sequence': self.sequence + 1,
            'theme_mode': theme_style.theme_mode.id,
        })

        return new_style.get_style()
