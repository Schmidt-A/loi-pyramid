import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized
from pyramid.view import view_config, view_defaults

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Account
from ..decorators import set_authorized
from ..schemas import AccountUpdateSchema, Invalid


log = logging.getLogger(__name__)

#Govern calls to a single account object /account/{username}
@set_authorized
@view_defaults(route_name='account', renderer='json')
class AccountViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Account)
            account = query.filter(Account.username == self.url['username']).one()
            log.info(
                'get: username {}'.format(account.username))

        except NoResultFound:
            log.error(
                'get: account \'{}\' not found'.format(self.url['username']))
            raise HTTPNotFound

        return account

#Govern calls to all account objects /accounts
@set_authorized
@view_defaults(route_name='accounts', renderer='json')
class AccountsViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Account)
            accounts = query.all()
            log.info('get: all accounts')

        except NoResultFound:
            log.error('get: could not retrieve any accounts')
            raise HTTPNotFound

        return accounts
