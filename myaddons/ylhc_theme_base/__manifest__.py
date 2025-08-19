# -*- coding: utf-8 -*-
{
    'name': "ylhc_theme_base",

    'summary': """
        Base for themes, it support free login for odoo
    """,

    'description': """
        Odoo Login, 
        Odoo login page, 
        Odoo login theme
        Login, 
        ylhc Theme Base,
        ylhc Theme,
        Ylhc Theme,
        Multi tab theme,
        Pop form theme
    """,

    'author': "ylhctec",

    'website': "https://www.ylhctec.com",
    'live_test_url': 'https://www.ylhctec.com',

    'license': 'OPL-1',
    'images': ['static/description/screen_shot.png', 'static/description/banner.png'],
    'support': 'codercrax@gmail.com',
    'maintainer': 'ylhctec',
    'category': 'Theme/Backend',
    'version': '17.0.0.3',

    'installable': True,
    'application': True,
    'auto_install': False,

    'depends': ['base', 'web'],
    
    'data': [],

    'assets': {
        'web.assets_backend': [
            'ylhc_theme_base/static/css/ylhc_variables.scss',
            'ylhc_theme_base/static/css/mixins/_flex.scss',
            'ylhc_theme_base/static/css/mixins/_box_shadow.scss',
            'ylhc_theme_base/static/css/mixins/_clearfix.scss',
            'ylhc_theme_base/static/css/mixins/_float.scss',
            'ylhc_theme_base/static/css/mixins/_hover.scss',
            'ylhc_theme_base/static/css/mixins/_gradients.scss',

            'ylhc_theme_base/static/css/ylhc_functions.scss',
            'ylhc_theme_base/static/css/ylhc_form_controls.scss',

            'ylhc_theme_base/static/css/ylhc_scroll.scss',
            'ylhc_theme_base/static/css/ylhc_misc.scss',
        ]
    }
}
