from flask import json, Response
from typing import Dict


class ApiResponse(Response):

    def __init__(self, data: Dict, status: int = 200, *,
                 warnings=None, meta=None, links=None, pagination=None, headers=None):

        resp = {
            'data': data,
            'warnings': warnings,
            '_meta': meta,
            '_links': links,
            '_pagination': pagination
        }

        super().__init__(json.dumps({k: v for (k, v) in resp.items()
                                     if v is not None and len(v) > 0}),
                         status=status, mimetype='application/json', headers=headers)
