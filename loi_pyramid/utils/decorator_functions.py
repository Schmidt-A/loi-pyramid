import re

from pyramid.httpexceptions import HTTPInternalServerError, HTTPUnauthorized

VIEW_MODULE_REGEX = r'loi_pyramid\.views\.[a-z]+'


def authorized(view_func):
    def wrapped(*args, **kw):
        if not _valid_auth_args(args):
            raise HTTPInternalServerError

        if not args[0].request.authenticated_userid:
            raise HTTPUnauthorized

        return view_func(*args, **kw)
    return wrapped

def needs_auth(val, attr):
    if attr.startswith('__') or hasattr(val, '_ignore_auth'):
        return False
    return True


def _valid_auth_args(args):
    if len(args) < 1:
        return False
    if not re.match(VIEW_MODULE_REGEX, args[0].__module__):
        return False
    return True
