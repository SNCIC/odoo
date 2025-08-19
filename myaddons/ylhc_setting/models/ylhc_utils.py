# -*- coding: utf-8 -*-

from odoo import fields
from datetime import date, datetime

def sanitize_record_datas(datas):
    """
    Sanitize Data
    :param data:
    :return:
    """
    if not isinstance(datas, list):
        datas = [datas]

    for index, data in enumerate(datas):
        if isinstance(data, dict):
            for key, item in data.items():
                if isinstance(item, datetime):
                    data[key] = fields.Datetime.to_string(item)
                if isinstance(item, date):
                    data[key] = fields.Date.to_string(item)
                # check if it is a list
                if isinstance(item, list):
                    sanitize_record_datas(item)
                # check if it is a dict
                if isinstance(item, dict):
                    sanitize_record_datas(item)
        elif isinstance(data, list):
            sanitize_record_datas(data)
        elif isinstance(data, datetime):
            datas[index] = fields.Datetime.to_string(data)
        elif isinstance(data, date):
            datas[index] = fields.Date.to_string(data)
        elif isinstance(data, bytes):
            datas[index] = data.decode('utf-8')

