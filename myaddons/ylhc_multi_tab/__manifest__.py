# -*- coding: utf-8 -*-
{
    'name': "ylhc_multi_tab",

    'summary': """
        ylhc multi tab plugin for odoo""",

    'description': """
        ylhc multi tab plugin
        multi tab,
        multi tab theme,
        odoo theme
    """,

    'author': 'ylhctec',
    'website': 'https://www.ylhctec.com',
    'live_test_url': 'https://www.ylhctec.com',

    'category': 'Backend/Theme',
    'version': '18.0.0.1',
    'license': 'OPL-1',
    'images': ['static/description/banner.png',
               'static/description/ylhc_screenshot.png'],

    'depends': ['base','web'],

    "application": False,
    "installable": True,
    "auto_install": False,

    'price': 999.00,
    'currency': 'USD',
    
    'data': [],

    'assets': {
        'web.assets_backend': [
    
            'ylhc_multi_tab/static/src/components/multi_tab/ylhc_multi_tab.scss',
            'ylhc_multi_tab/static/src/ylhc_action_container.scss',

            'ylhc_multi_tab/static/src/components/multi_tab/ylhc_multi_tab.js',
            'ylhc_multi_tab/static/src/components/multi_tab/ylhc_multi_tab.xml',
            
            'ylhc_multi_tab/static/src/ylhc_action_container.js',
            'ylhc_multi_tab/static/src/ylhc_action_service.js',
            'ylhc_multi_tab/static/src/ylhc_list_patch.js'
        ]
    }
}
