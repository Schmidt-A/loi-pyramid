# flake8: noqa
import copy

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.account import AccountViews
from ..views.account import AccountsViews
from ..security import hash_password
from .fixture_helper import FixtureHelper


class TestAccountViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestAccountViews, self).setUp()
        self.init_database()

        from ..models import Account

        self.host = 'http://localhost:6543'

        self.accounts = FixtureHelper.account_data(self)
        for key, account in self.accounts.items():
            self.session.add(account)

        self.session.flush()

        #non existent accounts, to be used for negative testing
        self.fake_accounts = FixtureHelper.fake_account_data(self)

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

    #Test that we can get Tweek via get call
    def test_get(self):
        account_result = self.account_get(self.accounts.get('tweek'))

        self.assertEqual(account_result['username'], self.accounts.get('tweek').username)
        self.assertEqual(account_result['password'], self.accounts.get('tweek').password)
        self.assertEqual(account_result['cdkey'], self.accounts.get('tweek').cdkey)
        self.assertEqual(account_result['role'], self.accounts.get('tweek').role)
        self.assertEqual(account_result['approved'], self.accounts.get('tweek').approved)
        self.assertEqual(account_result['banned'], self.accounts.get('tweek').banned)

    #Test that we cannot get Tam via get call
    #Because he'll never nut up and log on
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.account_get(self.fake_accounts.get('tam'))

    #Test that we can get all one account via get all call
    #As those are the only two created accounts
    def test_get_all(self):
        accounts_result = self.accounts_get_all()

        self.assertEqual(len(accounts_result), 3)
        tweek = accounts_result[0]
        aez = accounts_result[1]
        noob = accounts_result[2]

        self.assertEqual(tweek['username'], self.accounts.get('tweek').username)
        self.assertEqual(tweek['password'], self.accounts.get('tweek').password)
        self.assertEqual(tweek['cdkey'], self.accounts.get('tweek').cdkey)
        self.assertEqual(tweek['role'], self.accounts.get('tweek').role)
        self.assertEqual(tweek['approved'], self.accounts.get('tweek').approved)
        self.assertEqual(tweek['banned'], self.accounts.get('tweek').banned)

        self.assertEqual(aez['username'], self.accounts.get('aez').username)
        self.assertEqual(aez['password'], self.accounts.get('aez').password)
        self.assertEqual(aez['cdkey'], self.accounts.get('aez').cdkey)
        self.assertEqual(aez['role'], self.accounts.get('aez').role)
        self.assertEqual(aez['approved'], self.accounts.get('aez').approved)
        self.assertEqual(aez['banned'], self.accounts.get('aez').banned)

        self.assertEqual(noob['username'], self.accounts.get('noob').username)
        self.assertEqual(noob['password'], self.accounts.get('noob').password)
        self.assertEqual(noob['cdkey'], self.accounts.get('noob').cdkey)
        self.assertEqual(noob['role'], self.accounts.get('noob').role)
        self.assertEqual(noob['approved'], self.accounts.get('noob').approved)
        self.assertEqual(tweek['banned'], self.accounts.get('tweek').banned)
