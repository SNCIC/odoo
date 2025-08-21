# -*- coding: utf-8 -*-
{
    'name': "ylhc_setting",

    'summary': """
        ylhc theme
        advance theme
        sunsine theme
        mnk theme for odoo
        free backend theme
        odoo theme
        owl theme
        multi mode theme
        free theme
        multi style theme
        button style theme
        crazy theme
        nice theme
        mutli tab theme
        multi layout theme
        mult tab style theme
    """,

    'description': """
        ylhctec theme setting for odoo, it is a powerfull theme
    """,

    'author': "ylhctec",
    'website': "https://www.ylhctec.com",
    'live_test_url': 'https://www.ylhctec.com',
    'images': [
        'static/description/screen_shot.png',
        'static/description/banner.png', 
    ],
    'license': 'OPL-1',

    'category': 'Themes/Backend',
    'version': '18.5.0.3',
    'price': 999,

    'depends': ['web'],

    'data': [
        'security/ir.model.access.csv',
        'data/theme_data.xml',

        'views/ylhc_theme_mode.xml',
        'views/ylhc_theme_style.xml',
        'views/ylhc_theme_var.xml',
        'views/ylhc_web.xml',
        'views/ylhc_image_wizard.xml',
        'views/ylhc_res_setting.xml',

        'views/ylhc_ui_menu.xml',
    ],

    'assets': {

        'web.assets_backend': [

            # aniate.css
            'ylhc_setting/static/libs/animate.css',

            # theme customizer
            'ylhc_setting/static/src/components/customizer/*',
            'ylhc_setting/static/src/components/settings/*.js',
            'ylhc_setting/static/src/components/settings/*.xml',

            'ylhc_setting/static/src/ylhc_theme_setting.js',

            # according
            'ylhc_setting/static/src/components/accordion/*',

            # dialog
            'ylhc_setting/static/src/components/dialog/*',

            # color picker
            'ylhc_setting/static/src/components/color_picker/color_picker.js',
            'ylhc_setting/static/src/components/color_picker/color_picker.xml',
            'ylhc_setting/static/src/components/color_picker/color_picker.scss',
            
            'ylhc_setting/static/libs/spectrum.js',
            'ylhc_setting/static/libs/spectrum.css',
            'ylhc_setting/static/src/ylhc_icon.js',

            # client
            'ylhc_setting/static/src/components/webclient/webclient.js',
        ],

        'web.assets_web': [
             ('replace', 'web/static/src/main.js', 'ylhc_setting/static/src/ylhc_main.js'),
        ]
    }
}
