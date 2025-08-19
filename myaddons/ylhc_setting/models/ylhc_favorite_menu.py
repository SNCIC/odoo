# -*- coding: utf-8 -*-

from odoo import api, fields, models


class YlhcFavoriteMenu(models.Model):
    '''
    user favorite menu
    '''
    _name = 'ylhc_setting.favorite_menu'
    _order = "sequence"
    _description = "user favorite menu"

    def _default_sequence(self):
        """
        default sequence
        """
        return self.env['ir.sequence'].next_by_code('ylhc_setting.favorite.menu')

    sequence = fields.Integer(
        string="sequence",
        default=_default_sequence)

    menu_id = fields.Many2one(
        comodel_name='ir.ui.menu',
        string='Favorite Menu',
        required=True,
        ondelete='cascade')

    user_id = fields.Many2one(
        comodel_name='res.users', 
        string='User Name', 
        default=lambda self: self.env.user.id)

    @api.model
    def unlink_menu_id(self, user_id, menu_id):
        '''
        unlink
        :param user_id:
        :param menu_id:
        :return:
        '''
        value = self.search(
            [('menu_id', '=', menu_id), ('user_id', '=', user_id)])
        return value.unlink()
    
    @api.model
    def update_favorite_menu(self, favorites):
        '''
        update favoirte
        :return: 
        '''
        records = self.search([('user_id', '=', self.env.uid)])
        records.unlink()
        self.create(favorites)
        return self.search_read([('user_id', '=', self.env.uid)])
