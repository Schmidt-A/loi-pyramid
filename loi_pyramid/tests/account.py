# flake8: noqa
import copy

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.account import AccountViews
from ..views.account import AccountsViews
from ..security import hash_password


class TestAccountViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestAccountViews, self).setUp()
        self.init_database()

        from ..models import Account

        self.host = 'http://localhost:6543'

        fixture = []
        self.tweek = Account(
                username    = 'Tweek',
                password    = '$2b$12$rHfWWZ0quR5x48479dwPBekHeiuhdBtT8A4IQKTC32ifOxhG0FKxK'.encode('utf8'),
                cdkey       = 'efgh5678',
                role        = 3,
                approved    = 1,
                banned      = 0)
        fixture.append(self.tweek)

        self.session.add_all(fixture)
        self.session.flush()

        #non existent account, to be used for negative testing
        self.tam = Account(
                username    = 'TamTamTamTam',
                password    = '$2b$12$aVzX7hfREVbVNy/UsAIUCu86tw23661kTl8iED8d1TbzreEWp9P0C'.encode('utf8'),
                cdkey       = 'yzyz8008',
                role        = 1,
                approved    = 0,
                banned      = 0)

    #Helper method for get calls to /account/{username}
    def account_get(self, account):
        resource = '/account/{}'.format(account.username)
        url_params = {'username': account.username}
        request = self.dummy_request(self.session, (self.host+resource))

        account_view = AccountViews(testing.DummyResource(), request)
        account_view.url = url_params

        account_result = account_view.get().__json__(request)
        return account_result

    #Helper method for get all calls to /accounts
    def accounts_get_all(self):
        resource = '/accounts'
        request = self.dummy_request(self.session, (self.host+resource))

        account_view = AccountsViews(testing.DummyResource(), request)

        accounts_get = []
        for account in account_view.get():
            accounts_get.append(account.__json__(request))

        return accounts_get

    #Test that we can get Siobhan via get call
    def test_tweek_get(self):
        account_result = self.account_get(self.tweek)

        self.assertEqual(account_result['username'], self.tweek.username)
        self.assertEqual(account_result['password'], self.tweek.password)
        self.assertEqual(account_result['cdkey'], self.tweek.cdkey)
        self.assertEqual(account_result['role'], self.tweek.role)
        self.assertEqual(account_result['approved'], self.tweek.approved)
        self.assertEqual(account_result['banned'], self.tweek.banned)

    #Test that we cannot get Tam via get call
    #Because he'll never nut up and log on
    def test_tam_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.account_get(self.tam)

    #Test that we can get all one account via get all call
    #As those are the only one created account
    def test_all_six_accounts_get(self):
        accounts_result = self.accounts_get_all()

        self.assertEqual(len(accounts_result), 1)
        tweek = accounts_result[0]

        self.assertEqual(tweek['username'], self.tweek.username)
        self.assertEqual(tweek['password'], self.tweek.password)
        self.assertEqual(tweek['cdkey'], self.tweek.cdkey)
        self.assertEqual(tweek['role'], self.tweek.role)
        self.assertEqual(tweek['approved'], self.tweek.approved)
        self.assertEqual(tweek['banned'], self.tweek.banned)
