# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import AccessError
from odoo.models import check_method_name


class AnitaViewExtend(models.Model):
    '''
    anita view extend current_theme_mode
    '''
    _inherit = 'ir.ui.view'

    def _render_template(self, template, values=None):
        """
        rewrite to change the title
        :param template:
        :param values:
        :param engine:
        :return:
        """
        
        if template in ['web.login', 'web.webclient_bootstrap']:
            if not values:
                values = {}
            values["title"] = self.env['ir.config_parameter'].sudo().get_param(
                "anita_theme_base.window_default_title", "openErpNext")

        return super(AnitaViewExtend, self)._render_template(
            template, values=values)
