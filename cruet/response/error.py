import sys
from flask import Response, json, current_app
from werkzeug.exceptions import HTTPException
from typing import Dict, List


class ApiError(HTTPException):
    def __init__(self, message: str, status: int = 500, *, extra: Dict = None, headers: List = None) -> None:
        """ If used with flask-restful, the data field is being returned"""
        self._headers = headers

        resp = {
            'message': message,
            'extra': extra
        }

        self.code = status
        self.description = resp['message']  # to make it compliant with general HTTPException use
        self.data = {k: v for k, v in resp.items() if v is not None}

    def to_dict(self):
        return self.data

    def get_response(self, environ=None):
        return Response(json.dumps(self.to_dict()),
                        status=self.code, mimetype='application/json',
                        headers=self._headers)

    def handle_error(self):
        """log and return response"""
        if self.code and self.code >= 500:
            exc_info = sys.exc_info()
            if exc_info[1] is None:
                exc_info = None
            current_app.log_exception(exc_info)
        return self.get_response()


def register_api_error(app):
    app.register_error_handler(ApiError, lambda err: err.handle_error())
