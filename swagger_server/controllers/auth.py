# coding: utf-8
from swagger_server.config import settings


def api_key(key, required_scopes=None):
    if settings.AUTHORIZATION == key:
        return {'sub': 'admin'}

    # optional: raise exception for custom error response
    return None
