# -*- coding: utf-8 -*-
from werkzeug.exceptions import HTTPException


class AppBaseException(HTTPException):
    def __init__(self, code, description, data=None, extra_info=None):
        self.code = int(code)
        self.description = description
        self.response = data
        self.extra_info = extra_info


class ParameterError(AppBaseException):
    pass


def return_function(meta_code, error_code, error_message):
    return_dict = {
        'code': meta_code,
        'error_code': error_code,
        'error_message': error_message
    }
    return return_dict
