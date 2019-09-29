import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Account, Character

log = logging.getLogger(__name__)

#Govern calls to a single account object /accounts/{username}
@view_defaults(route_name='account', renderer='json')
class AccountViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
       return self.get_one(Account)


#Govern calls to all account objects /accounts
#By default, limit of 10
@view_defaults(route_name='accounts', renderer='json')
class AccountsViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all(Account)

#Govern calls to all characters under an account /accounts/{username}/characters
@view_defaults(route_name='account_characters', renderer='json')
class AccountCharactersView(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all_by_one(Account, Character)
