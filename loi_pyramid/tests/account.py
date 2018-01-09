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

        return account_view.get().json_body

    #Helper method for get all calls to /accounts
    def accounts_get_all(self, user_account):
        resource = '/accounts'
        request = self.dummy_request(self.session, (self.host+resource), user_account)

        account_view = AccountsViews(testing.DummyResource(), request)

        return account_view.get().json_body

    #Helper method for get all calls to /account/{username}/characters
    def account_characters_get_all(self, account, user_account):
        resource = '/account/{}/characters'.format(account['username'])
        url_params = {'username': account['username']}
        request = self.dummy_request(self.session, (self.host+resource), user_account)

        account_view = AccountCharactersViews(testing.DummyResource(), request)
        account_view.url = url_params

        return account_view.get().json_body

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

        compare_items = []
        for key, item in self.items.items():
            if item['characterId'] == self.characters['jilin']['id']:
                compare_items.append(item)

        self.assertEqual(len(items_result), len(compare_items))
        i = 0
        for item in items_result:
            compare_item = compare_items[i]
            self.assertEqual(item['username'], compare_item['username'])
            self.assertEqual(item['username'], compare_item['password'])
            self.assertEqual(item['username'], compare_item['cdkey'])
            self.assertEqual(item['username'], compare_item['role'])
            self.assertEqual(item['username'], compare_item['approved'])
            self.assertEqual(item['username'], compare_item['banned'])
            i += 1
