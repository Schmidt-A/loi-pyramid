# flake8: noqa
import copy

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.account import AccountViews, AccountsViews, AccountCharactersView
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
        self.characters = self.fixture_helper.character_data()
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
    def characters_get_all(self, account, user_account):
        resource = '/account/{}/characters'.format(account['username'])
        url_params = {'username': account['username']}
        request = self.dummy_request(self.session, (self.host+resource), user_account)

        account_view = AccountCharactersView(testing.DummyResource(), request)
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

    #Test that we can get all accounts via get all call
    #As those are the only two created accounts
    def test_get_all(self):
        accounts_result = self.accounts_get_all(self.accounts['tweek'])

        compare_accounts = list(self.accounts.values())

        self.assertEqual(len(accounts_result), len(compare_accounts))
        i = 0
        for account in accounts_result:
            compare_account = compare_accounts[i]
            self.assertEqual(account['username'], compare_account['username'])
            self.assertEqual(account['cdkey'], compare_account['cdkey'])
            self.assertEqual(account['role'], compare_account['role'])
            self.assertEqual(account['approved'], compare_account['approved'])
            self.assertEqual(account['banned'], compare_account['banned'])
            i += 1

    #Test that we can get all characters for Tweek via get all call
    def test_get_all_chars(self):
        characters_result = self.characters_get_all(self.accounts['tweek'], self.accounts['tweek'])

        compare_chars = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['tweek']['username']:
                compare_chars.append(char)

        self.assertEqual(len(characters_result), len(compare_chars))
        i = 0
        for char in compare_chars:
            compare_char = compare_chars[i]
            self.assertEqual(char['accountId'], compare_char['accountId'])
            self.assertEqual(char['name'], compare_char['name'])
            self.assertEqual(char['exp'], compare_char['exp'])
            self.assertEqual(char['area'], compare_char['area'])
            self.assertEqual(char['created'], compare_char['created'])
            self.assertEqual(char['updated'], compare_char['updated'])
            i += 1

    #Test that we cannot get Tam's characters via get all call
    #Because he never nutted up and logged on
    def test_get_all_chars_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.characters_get_all(self.fake_accounts['tam'], self.accounts['tweek'])
