import logging

from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import remember, forget
from pyramid.view import view_config, view_defaults

from . import BaseView
from ..security import USERS, check_password

from ..schemas import LoginSchema, Invalid


log = logging.getLogger(__name__)


@view_defaults(renderer='json')
class AuthViews(BaseView):

    @view_config(route_name='login', request_method='POST')
    def login(self):
        schema = LoginSchema()
        try:
            info = schema.deserialize(self.request.POST)
        except Invalid as e:
            log.error('Failed to deserialize login info: {}'.format(e))
            raise HTTPUnauthorized

        user = info['user']
        pw = info['pw']
        hashed_pw = USERS.get(user)

        if hashed_pw and check_password(pw, hashed_pw):
            headers = remember(self.request, user)
            return headers

        raise HTTPUnauthorized

    @view_config(route_name='logout', request_method='POST')
    def logout(self):
        headers = forget(self.request)
        return headers
