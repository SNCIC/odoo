# -*- coding: utf-8 -*-
from odoo import models, fields, api


class YlhcThemeVar(models.Model):
    '''
    user theme style setting
    '''
    _name = 'ylhc_setting.theme_var'
    _order = 'sequence asc'
    _description = "Theme Var"

    sequence = fields.Integer(string="sequence", default=0)
    category = fields.Char(string="Category", default="Others")

    theme_style_id = fields.Many2one(
        comodel_name="ylhc_setting.theme_style",
        string="Theme Style",
        ondelete="cascade")

    type = fields.Selection(
        selection=[('color', 'color'),
                   ('image', 'image'),
                   ('image_url', 'image_url'),
                   ('svg', 'svg')],
        string="type",
        default="color")

    name = fields.Char(string="Name", default="var1")
    color = fields.Char(string="Val")
    color_type = fields.Selection(
        selection=[
            ('background', 'background'), 
            ('text', 'text'), 
            ('border', 'border'), 
            ('shadow', 'shadow')], 
        default='background', string="color type", help="Type use to apply aphla!")
    disable_opacity = fields.Boolean(string="Disable Opacity", default=False)
    
    image = fields.Binary(string="image", attachment=True)
    image_file_url = fields.Char(string="Image File Url", compute="_compute_image_file_url")
    image_url = fields.Char(string="Image Url")
    svg = fields.Text(string="Svg")
    opacity = fields.Float(string="Opacity", default=1.0)
    alias = fields.Char(string="Alias")
    help = fields.Char(string="Help")

    value = fields.Char(string="Value", compute="_compute_value")

    identity = fields.Char(string="identify")
    is_default = fields.Boolean(string="is default", default=True)

    @api.depends('image')
    def _compute_image_file_url(self):
        """
        compute image file url
        :return:
        """
        for record in self:
            if record.type == 'image' and record.image:
                record.image_file_url = \
                    '/web/image/ylhc_setting.theme_var/{var_id}/image'.format(
                        var_id=record.id)
            else:
                record.image_file_url = False

    def get_edit_var_action(self):
        """
        get edit action
        :return:
        """
        return {
            "type": "ir.actions.act_window",
            "res_model": "ylhc_setting.theme_var",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
            "views": [[self.env.ref(
                'ylhc_setting.edit_theme_var_form').id, "form"]]
        }

    def reset_var(self):
        """
        reset var
        :return:
        """
        if not self.ref_var and self.type != 'color':
            return False
        # get mode first
        var_cache = self.style_item.sub_group.group.theme_style.theme_mode.get_scss_vars_cache()
        if self.ref_var in var_cache:
            self.color = var_cache.get(self.ref_var, False)
        return True
    
    @api.depends('color', 'image', 'image_url', 'svg', 'opacity')
    def _compute_value(self):
        """
        compute value
        :return:
        """
        for record in self:
            if record.type == 'color':
                record.value = record.color
            elif record.type == 'image':
                record.value = record.image
            elif record.type == 'image_url':
                record.value = record.image_file_url
            elif record.type == 'svg':
                record.value = record.svg
            else:
                record.value = False

