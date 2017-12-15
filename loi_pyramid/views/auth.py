import logging

from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.view import view_config, view_defaults

from . import BaseView
from ..decorators import set_authorized, no_auth
from ..security import USERS, check_password

from ..schemas import LoginSchema, Invalid


log = logging.getLogger(__name__)


@set_authorized
class AuthViews(BaseView):

    @no_auth
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
            print(self.request)
            response = Response(headers=headers)
            print(response)
            return response

        return HTTPUnauthorized()

    # TODO: this should be a POST but for facilitating testing, GET for now
    @view_config(route_name='logout', request_method='GET')
    def logout(self):
        headers = forget(self.request)
        return Response(headers=headers)
