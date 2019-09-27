import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Account, Character
from ..schemas import AccountAdminUpdate, AccountOwnerUpdate, Invalid


log = logging.getLogger(__name__)

#Govern calls to a single account object /accounts/{username}
@view_defaults(route_name='account', renderer='json')
class AccountViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Account)
            account = query.filter(Account.username == self.url['username']).one()
            log.debug(
                'get: username {}'.format(account.username))

            #if they own it or they're an admin
            #infuriatingly, unittest does not recognize the valid character.account relationship
            if self.request.account == account or self.request.account.is_admin():
                response = Response(json=account.owned_payload, content_type='application/json')

            else:
                response = Response(json=account.public_payload, content_type='application/json')

        except NoResultFound:
            log.debug(
                'get: account \'{}\' not found'.format(self.url['username']))
            raise HTTPNotFound

        return response


#Govern calls to all account objects /accounts
@view_defaults(route_name='accounts', renderer='json')
class AccountsViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Account)
            accounts = query.all()
            log.debug('get: all accounts')

            get_all_data = []
            for account in accounts:
                #if they're an admin they can see everything
                if self.request.account.is_admin():
                    get_all_data.append(account.owned_payload)

                else:
                    get_all_data.append(account.public_payload)

            response = Response(json=get_all_data, content_type='application/json')

        except NoResultFound:
            log.error('get: could not retrieve any accounts')
            raise HTTPNotFound

        return response

#Govern calls to all characters under an account /accounts/{username}/characters
@view_defaults(route_name='account_characters', renderer='json')
class AccountCharactersView(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            #only doing this because otherwise the NoResultFound won't throw - might refactor by making it an if character returned
            query = self.request.dbsession.query(Account)
            account = query.filter(Account.username == self.url['username']).one()

            char_query = self.request.dbsession.query(Character)
            characters = char_query.filter(Character.accountId == self.url['username']).all()

            log.debug(
                'get: characters of {}'.format(self.url['username']))

            get_all_data = []
            for character in characters:
                if self.request.account == account or self.request.account.is_admin():
                    get_all_data.append(character.owned_payload)

                else:
                    get_all_data.append(character.public_payload)

            response = Response(json=get_all_data, content_type='application/json')

        except NoResultFound:
            log.debug(
                'get: no characters found with account {}'.format(self.url['username']))
            get_all_data = []
            response = Response(json=get_all_data, content_type='application/json')

        return response
