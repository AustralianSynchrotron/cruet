import wrapt
from inspect import getfullargspec
from flask import request
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from cruet import ApiError


def dataschema(schema, format: str = 'json', unknown=EXCLUDE, error_class=ApiError):
    """ Decorator for input validation of endpoints.
    Requires marshmallow 3
    """
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        if format == 'json':
            try:
                data = request.get_json()
                if data is None:
                    if request.mimetype != 'application/json':
                        raise error_class(
                            'Mimetype application/json expected but {} found'.
                            format(request.mimetype), 400)
                    raise error_class('No JSON found in the request body', 400)
            except BadRequest as e:
                raise error_class('The payload must be valid json and ' +
                               'the mimetype "application/json"', 400,
                               extra=e.description)
        elif format == 'param':
            data = request.values.to_dict()
        else:
            raise RuntimeError('format has to be either param or json')

        try:
            data_validated = schema.load(data, unknown=unknown)
            keys_excluded = (data.keys() - data_validated.keys())\
                if unknown == EXCLUDE else set()

        except ValidationError as e:
            raise error_class('Validation of input failed', 400, extra=e.messages)

        # update keyword args for the decorated function
        new_kwargs = {}
        wrapped_args = getfullargspec(wrapped).args
        if 'data' in wrapped_args:
            new_kwargs['data'] = data_validated

        if 'excluded' in wrapped_args:
            new_kwargs['excluded'] = keys_excluded

        kwargs.update(new_kwargs)

        return wrapped(*args, **kwargs)
    return wrapper
