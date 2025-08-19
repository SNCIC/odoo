# -*- coding: utf-8 -*-
{
    'name': "ylhc_login",

    'summary': """
        Login Pages For Odoo
    """,

    'description': """
        Login Pages For Odoo
    """,

    'author': "ylhc",
    'website': "https://www.openerpnext.com",

    'category': 'Theme/Backend',
    'version': '17.0.0.3',
    'license': 'OPL-1',
    'images': [
        'static/description/banner.png',
        'static/description/ylhc_screenshot.png'
    ],

    'depends': ['base', 'web'],

    'data': [
        "views/login_style1.xml"
    ],

    'assets': {
        'web.assets_backend': [],
    }
}
