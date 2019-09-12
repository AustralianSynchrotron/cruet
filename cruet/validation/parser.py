from functools import partial
from webargs.flaskparser import FlaskParser

from cruet import ApiError


class CruetParser(FlaskParser):
    def parse_json(self, req, name, field):
        """Pull a json value from the request."""
        json_data = self._cache.get('json')
        if json_data is None:
            if not req.is_json:
                raise ApiError('Mimetype application/json expected but {} found.'.format(req.mimetype), 400)
        return super().parse_json(req, name, field)

    def handle_error(self, error, req, schema, error_status_code, error_headers):
        """Handles errors during parsing. """
        raise ApiError(error.messages, error_status_code or self.DEFAULT_VALIDATION_STATUS)

    def handle_invalid_json_error(self, error, req, *args, **kwargs):
        raise ApiError('Invalid JSON body.', 400)


parser = CruetParser()

use_args = parser.use_args
use_kwargs = parser.use_kwargs

# convenient decorators
body = partial(use_args, locations=('json',))
query = partial(use_args, locations=('query',))
form = partial(use_args, locations=('form',))
