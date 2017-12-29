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

        fixture_data = FixtureHelper(self.session)
        self.accounts = fixture_data.account_data()

        self.session.flush()

        #non existent accounts, to be used for negative testing
        self.fake_accounts = fixture_data.fake_account_data()

    #Helper method for get calls to /account/{username}
    def account_get(self, account, user_account):
        resource = '/account/{}'.format(account.get('username'))
        url_params = {'username': account.get('username')}
        request = self.dummy_request(self.session, (self.host+resource), user_account)

        account_view = AccountViews(testing.DummyResource(), request)
        account_view.url = url_params

        account_result = account_view.get().__json__(request)
        return account_result

    #Helper method for get all calls to /accounts
    def accounts_get_all(self, user_account):
        resource = '/accounts'
        request = self.dummy_request(self.session, (self.host+resource), user_account)

        account_view = AccountsViews(testing.DummyResource(), request)

        accounts_get = []
        for account in account_view.get():
            accounts_get.append(account.__json__(request))

        return accounts_get

    #Test that we can get Tweek via get call
    def test_get(self):
        account_result = self.account_get(self.accounts.get('tweek'), self.accounts.get('tweek'))

        self.assertEqual(account_result['username'], self.accounts.get('tweek').get('username'))
        self.assertEqual(account_result['password'], self.accounts.get('tweek').get('password'))
        self.assertEqual(account_result['cdkey'], self.accounts.get('tweek').get('cdkey'))
        self.assertEqual(account_result['role'], self.accounts.get('tweek').get('role'))
        self.assertEqual(account_result['approved'], self.accounts.get('tweek').get('approved'))
        self.assertEqual(account_result['banned'], self.accounts.get('tweek').get('banned'))

    #Test that we cannot get Tam via get call
    #Because he'll never nut up and log on
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.account_get(self.fake_accounts.get('tam'), self.accounts.get('tweek'))

    #Test that we can get all one account via get all call
    #As those are the only two created accounts
    def test_get_all(self):
        accounts_result = self.accounts_get_all(self.accounts.get('tweek'))

        self.assertEqual(len(accounts_result), 3)
        tweek = accounts_result[0]
        aez = accounts_result[1]
        noob = accounts_result[2]

        self.assertEqual(tweek['username'], self.accounts.get('tweek').get('username'))
        self.assertEqual(tweek['password'], self.accounts.get('tweek').get('password'))
        self.assertEqual(tweek['cdkey'], self.accounts.get('tweek').get('cdkey'))
        self.assertEqual(tweek['role'], self.accounts.get('tweek').get('role'))
        self.assertEqual(tweek['approved'], self.accounts.get('tweek').get('approved'))
        self.assertEqual(tweek['banned'], self.accounts.get('tweek').get('banned'))

        self.assertEqual(aez['username'], self.accounts.get('aez').get('username'))
        self.assertEqual(aez['password'], self.accounts.get('aez').get('password'))
        self.assertEqual(aez['cdkey'], self.accounts.get('aez').get('cdkey'))
        self.assertEqual(aez['role'], self.accounts.get('aez').get('role'))
        self.assertEqual(aez['approved'], self.accounts.get('aez').get('approved'))
        self.assertEqual(aez['banned'], self.accounts.get('aez').get('banned'))

        self.assertEqual(noob['username'], self.accounts.get('noob').get('username'))
        self.assertEqual(noob['password'], self.accounts.get('noob').get('password'))
        self.assertEqual(noob['cdkey'], self.accounts.get('noob').get('cdkey'))
        self.assertEqual(noob['role'], self.accounts.get('noob').get('role'))
        self.assertEqual(noob['approved'], self.accounts.get('noob').get('approved'))
        self.assertEqual(tweek['banned'], self.accounts.get('tweek').get('banned'))
