__version__ = "0.0.3"

from .response import ApiResponse, ApiError, register_api_error
from .validation import parser, use_args, use_kwargs, body, query, form

__all__ = ('ApiResponse', 'ApiError', 'parser', 'use_args', 'use_kwargs', 'body', 'query', 'form')


class Cruet:
    """ This class is used to control the Cruet integration to one or more Flask applications. """
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """This callback can be used to initialize an application for the
        use with cruet.
        """
        register_api_error(app)
