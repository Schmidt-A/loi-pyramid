import logging

from pyramid.httpexceptions import HTTPUnauthorized, HTTPClientError
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.view import view_config, view_defaults

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..decorators import set_authorized, no_auth
from ..security import check_password
from ..schemas import LoginSchema, AccountAdminUpdate, Invalid
from ..models import Account


log = logging.getLogger(__name__)


@set_authorized
class AuthViews(BaseView):

    @no_auth
    @view_config(route_name='login', request_method='POST')
    def login(self):
        schema = LoginSchema()
        info = {}
        try:
            info = schema.deserialize(self.request.POST)
        except Invalid as e:
            log.error('Failed to deserialize login info: {}'.format(e))
            raise HTTPClientError

        user = info['user']
        pw = info['pw']

        try:
            query = self.request.dbsession.query(Account)
            account = query.filter(Account.username == user).one()
            hashed_pw = account.password.decode('utf8')

            if hashed_pw and check_password(pw, hashed_pw):
                headers = remember(self.request, user)
                response = Response(headers=headers)

                log.info(
                    'login: username {}'.format(account.username))
                return response
            else:
                log.warn(
                    'login: username {} or password incorrect'.format(user))
                raise HTTPUnauthorized

        except NoResultFound as e:
            log.warn(
                'login: account \'{}\' not found'.format(user))
            raise HTTPUnauthorized

        return HTTPUnauthorized()

    # TODO: this should be a POST but for facilitating testing, GET for now
    @view_config(route_name='logout', request_method='GET')
    def logout(self):
        headers = forget(self.request)
        return Response(headers=headers)
