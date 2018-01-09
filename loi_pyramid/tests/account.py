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

        self.accounts = self.fixture_helper.account_data()
        self.session.flush()

        #non existent accounts, to be used for negative testing
        self.fake_accounts = self.fixture_helper.fake_account_data()

    #Helper method for get calls to /account/{username}
    def account_get(self, account, user_account):
        resource = '/account/{}'.format(account['username'])
        url_params = {'username': account['username']}
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
        account_result = self.account_get(self.accounts['tweek'], self.accounts['tweek'])

        self.assertEqual(account_result['username'], self.accounts['tweek']['username'])
        self.assertEqual(account_result['cdkey'], self.accounts['tweek']['cdkey'])
        self.assertEqual(account_result['role'], self.accounts['tweek']['role'])
        self.assertEqual(account_result['approved'], self.accounts['tweek']['approved'])
        self.assertEqual(account_result['banned'], self.accounts['tweek']['banned'])

    #Test that we cannot get Tam via get call
    #Because he'll never nut up and log on
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.account_get(self.fake_accounts['tam'], self.accounts['tweek'])

    #Test that we can get all one account via get all call
    #As those are the only two created accounts
    def test_get_all(self):
        accounts_result = self.accounts_get_all(self.accounts['tweek'])

        self.assertEqual(len(accounts_result), 3)
        tweek = accounts_result[0]
        aez = accounts_result[1]
        noob = accounts_result[2]

        self.assertEqual(tweek['username'], self.accounts['tweek']['username'])
        self.assertEqual(tweek['password'], self.accounts['tweek']['password'])
        self.assertEqual(tweek['cdkey'], self.accounts['tweek']['cdkey'])
        self.assertEqual(tweek['role'], self.accounts['tweek']['role'])
        self.assertEqual(tweek['approved'], self.accounts['tweek']['approved'])
        self.assertEqual(tweek['banned'], self.accounts['tweek']['banned'])

        self.assertEqual(aez['username'], self.accounts['aez']['username'])
        self.assertEqual(aez['password'], self.accounts['aez']['password'])
        self.assertEqual(aez['cdkey'], self.accounts['aez']['cdkey'])
        self.assertEqual(aez['role'], self.accounts['aez']['role'])
        self.assertEqual(aez['approved'], self.accounts['aez']['approved'])
        self.assertEqual(aez['banned'], self.accounts['aez']['banned'])

        self.assertEqual(noob['username'], self.accounts['noob']['username'])
        self.assertEqual(noob['password'], self.accounts['noob']['password'])
        self.assertEqual(noob['cdkey'], self.accounts['noob']['cdkey'])
        self.assertEqual(noob['role'], self.accounts['noob']['role'])
        self.assertEqual(noob['approved'], self.accounts['noob']['approved'])
        self.assertEqual(tweek['banned'], self.accounts['tweek']['banned'])
