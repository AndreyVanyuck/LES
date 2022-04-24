from typing import Dict, Iterable

from app.utils.enums import ErrorCodes


class BaseAPIException(Exception):
    status_code = 500
    success = False
    payload = []

    def __init__(self, message: str = '', payload: Dict = None, error_code: str = '', error_params: Iterable = ()):
        Exception.__init__(self)

        if error_code:
            enum_item = getattr(ErrorCodes, error_code, None)
            message = getattr(enum_item, 'value', '').format(*error_params)

            payload = {
                'error_code': error_code,
                'params': error_params
            }
        else:
            # deprecated
            if isinstance(payload, dict) and payload.get('error_code'):
                message = getattr(getattr(ErrorCodes, payload['error_code'], None), 'value', message)

        self.message = message
        self.payload = payload if payload else []

    def to_dict(self):
        return {
            'success': self.success,
            'payload': self.payload,
            'message': self.message
        }


class BadRequestAPIException(BaseAPIException):
    status_code = 400
