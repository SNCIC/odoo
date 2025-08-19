# -*- coding: utf-8 -*-

import odoo
import odoo.modules.registry
from odoo.tools.translate import _
from odoo.exceptions import AccessError
from odoo.addons.web.controllers.home import Home
from odoo import http
from odoo.http import request, Response
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools.misc import file_path

import logging
_logger = logging.getLogger(__name__)

try:
    from werkzeug.utils import send_file
except ImportError:
    from odoo.tools._vendor.send_file import send_file

import json
import base64
import functools
import io
import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))


class YlhcHome(Home):
    '''
    inherit home to extend web.login style
    '''
    @http.route([
        '/web/binary/logo_small',
        '/logo_small',
        '/logo_small.png',
    ], type='http', auth="none", cors="*")
    def company_logo(self, dbname=None, **kw):
        imgname = 'logo_small'
        imgext = '.png'
        default_logo = 'ylhc_setting/static/images/logo_small.png'
        dbname = request.db
        uid = (request.session.uid if dbname else None) or odoo.SUPERUSER_ID

        if not dbname:
            response = http.Stream.from_path(
                file_path(default_logo)).get_response()
        else:
            try:
                # create an empty registry
                registry = odoo.modules.registry.Registry(dbname)
                with registry.cursor() as cr:
                    company = int(kw['company']) if kw and kw.get('company') else False
                    if company:
                        cr.execute("""SELECT logo_small, write_date
                                        FROM res_company
                                       WHERE id = %s
                                   """, (company,))
                    else:
                        cr.execute("""SELECT c.logo_small, c.write_date
                                        FROM res_users u
                                   LEFT JOIN res_company c
                                          ON c.id = u.company_id
                                       WHERE u.id = %s
                                   """, (uid,))
                    row = cr.fetchone()
                    if row and row[0]:
                        image_base64 = base64.b64decode(row[0])
                        image_data = io.BytesIO(image_base64)
                        mimetype = guess_mimetype(image_base64, default='image/png')
                        imgext = '.' + mimetype.split('/')[1]
                        if imgext == '.svg+xml':
                            imgext = '.svg'
                        response = send_file(
                            image_data,
                            request.httprequest.environ,
                            download_name=imgname + imgext,
                            mimetype=mimetype,
                            last_modified=row[1],
                            response_class=Response,
                        )
                    else:
                        response = http.Stream.from_path(
                            file_path(default_logo)).get_response()
            except Exception as e:
                _logger.error(
                    "Error while retrieving company logo: %s", str(e))
                response = http.Stream.from_path(
                    file_path(default_logo)).get_response()

        return response
