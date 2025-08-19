# -*- coding: utf-8 -*-

from odoo import models, fields, api


class YlhcThemeSetting(models.Model):
    '''
    ylhc Setting Base
    '''
    _name = 'ylhc_setting.setting'
    _description = 'ylhc Setting'

    owner = fields.Reference(
        string="Owner",
        selection=[('res.company', 'res.company'),
                   ('res.users', 'res.users')],
        default=False,
        help="owner which this theme is create by, if it is false, it mean it is owned to the system!")

    layout_mode = fields.Char(
        string="Layout Mode",
        default='Layout1')

    control_panel_mode = fields.Char(
        string="Control Panel Mode",
        default='mode1')

    login_style = fields.Char(
        string="login style",
        default='login_style1')

    icon_policy = fields.Selection(
        string="Menu Icon Policy",
        selection=[
            ('web_icon', 'web_icon'),
            ('font_icon', 'font_icon'),
            ('svg_icon', 'svg_icon')],
        default='svg_icon')

    current_theme_mode = fields.Many2one(
        comodel_name='ylhc_setting.theme_mode',
        compute="_compute_current_theme_mode",
        string="Cur Theme Mode")

    current_theme_style = fields.Many2one(
        string="Current Theme Style",
        comodel_name="ylhc_setting.theme_style",
        domain="[('theme_mode', '=', current_theme_mode)]",
        help="Just use when theme style mode is system")

    dialog_animation_in_style = fields.Char(
        string="Dialog Animation In Style",
        default="animate__bounceIn")
    dialog_animation_out_style = fields.Char(
        string="Dialog Animation Out Style",
        compute="_compute_dialog_animation_out_style")

    button_style = fields.Char(
        string="Button Style",
        default="style1")

    input_style = fields.Char(
        string="Input Style",
        default="style1")

    tab_style = fields.Char(
        string="Tab Style",
        default="style1")
    
    font_name = fields.Char(
        string="Font Name",
        default="Roboto", help="Roboto, Helvetica, Verdana, Tahoma, OpenSans, Poppins, NotoSansArabic")

    loading_style = fields.Char(
        string="Loading Style",
        default="style1")

    loading_svg = fields.Char(string="Loading SVG", compute="_compute_loading_svg")

    checkbox_style = fields.Char(
        string="Checkbox Style",
        default="style1")

    radio_style = fields.Char(
        string="Radio Style",
        default="style1")

    separator_style = fields.Char(
        string="Separator Style",
        default="style1")

    rtl_mode = fields.Boolean(
        string="RTL MODE", 
        default=False)

    allow_debug = fields.Boolean(
        string="Allow Debug", 
        default=True)
    
    theme_mode_ids = fields.One2many(
        comodel_name="ylhc_setting.theme_mode",
        inverse_name="setting_id",
        string="Theme Models")
    
    @api.onchange('current_theme_mode')
    def on_current_theme_mode_change(self):
        """
        change the style
        :return:
        """
        if self.current_theme_mode.theme_styles:
            self.current_theme_style = \
                self.current_theme_mode.theme_styles[0].id
        else:
            self.current_theme_style = False

    @api.depends('loading_style')
    def _compute_loading_svg(self):
        """
        compute loading svg
        :return:
        """
        for rec in self:
            if rec.loading_style:
                rec.loading_svg = "/ylhc_setting/static/loadings/loading_%s.svg" % rec.loading_style
            else:
                rec.loading_svg = False

    @api.depends('dialog_animation_in_style')
    def _compute_dialog_animation_out_style(self):
        '''
        compute the dialog animation out style
        :return:
        '''
        for record in self:
            if record.dialog_animation_in_style:
                record.dialog_animation_out_style = record.dialog_animation_in_style.replace('In', 'Out')
            else:
                record.dialog_animation_out_style = 'animate__bounceOut'

    def ensure_current_theme_style(self):
        '''
        ensure current theme style
        :return:
        '''
        if not self.current_theme_style:
            if self.theme_mode_ids:
                theme_styles = self.theme_mode_ids[0].theme_styles
                if theme_styles:
                    self.current_theme_style = theme_styles[0]
                else:
                    self.current_theme_style = False
            else:
                self.current_theme_style = False

    @api.depends('current_theme_style')
    def _compute_current_theme_mode(self):
        '''
        compute current theme mode
        :return:
        '''
        for record in self:
            if record.current_theme_style:
                record.current_theme_mode = record.current_theme_style.theme_mode
            else:
                record.current_theme_mode = False