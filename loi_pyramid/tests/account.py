# flake8: noqa
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.account import AccountViews, AccountsViews, AccountCharactersView
from ..models import Account, Character

log = logging.getLogger(__name__)


class TestAccountViews(BaseTest):

    # Initial setup for these tests
    # Needs to be broken up
    def setUp(self):
        super(TestAccountViews, self).setUp()
        self.init_database()

        accounts_data = self.fixture_helper.account_data()
        characters_data = self.fixture_helper.character_data()
        self.session.flush()

        self.accounts = self.fixture_helper.convert_to_json(accounts_data)
        self.characters = self.fixture_helper.convert_to_json(characters_data)

        # non existent accounts, to be used for negative testing
        self.fake_accounts = self.fixture_helper.fake_account_fixture()

    # Helper method for get calls to /accounts/{username}
    def account_get(self, account, user_account):
        resources = [('accounts', ('username', account['username']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            account=user_account)

        account_view = AccountViews(testing.DummyResource(), request)

        return account_view.get().json_body

    # Helper method for get all calls to /accounts
    def accounts_get_all(self, user_account, limit=None, offset=None):
        resources = [('accounts', ('username', ''))]

        query = {}
        if limit is not None:
            query['limit'] = limit
        if offset is not None:
            query['offset'] = offset

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            query=query,
            account=user_account)

        account_view = AccountsViews(testing.DummyResource(), request)

        return account_view.get().json_body

    # Helper method for get all calls to /accounts/{username}/characters
    def characters_get_all(
            self,
            account,
            user_account,
            limit=None,
            offset=None):
        resources = [
            ('accounts', ('username', account['username'])),
            ('characters', ('charId', ''))]

        query = {}
        if limit is not None:
            query['limit'] = limit
        if offset is not None:
            query['offset'] = offset

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            query=query,
            account=user_account)

        account_view = AccountCharactersView(testing.DummyResource(), request)

        return account_view.get().json_body

    # Test that we can get Tweek via get call
    def test_get(self):
        account_result = self.account_get(
            self.accounts['tweek'], self.accounts['tweek'])

        self.assert_compare_objects(account_result, self.accounts['tweek'], 
            *Account.__owned__(Account))

    # Test that we cannot get Tam via get call
    # Because he'll never nut up and log on
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.account_get(self.fake_accounts['tam'], self.accounts['tweek'])

    # Test that we can get all accounts via get all call without limit
    def test_get_all(self):
        total = 10
        offset = 0
        accounts_result = self.accounts_get_all(self.accounts['tweek'])

        compare_accounts = list(self.accounts.values())[offset:offset + total]
        self.assertEqual(
            len(accounts_result['accounts']), len(compare_accounts))
        self.assertEqual(
            accounts_result['offset'],
            offset + len(compare_accounts))

        total_accounts = len(list(self.accounts.values()))
        self.assertEqual(accounts_result['total'], total_accounts)

        for account, compare_account in zip(
                accounts_result['accounts'], compare_accounts):
            self.assert_compare_objects(account, compare_account, 
                *Account.__owned__(Account))

    # Test that we can get all characters for Tweek via get all call
    def test_get_all_chars(self):
        total = 10
        offset = 0
        characters_result = self.characters_get_all(
            self.accounts['tweek'], self.accounts['tweek'])

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['tweek']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset + total]

        self.assertEqual(
            len(characters_result['characters']), len(compare_characters))
        self.assertEqual(
            characters_result['offset'],
            offset + len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        for character, compare_character in zip(
                characters_result['characters'], compare_characters):
            self.assert_compare_objects(character, compare_character, 
                *Character.__owned__(Character))

    # Test that we cannot get Tam's characters via get all call
    # Because he never nutted up and logged on
    def test_get_all_chars_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.characters_get_all(
                self.fake_accounts['tam'],
                self.accounts['tweek'])
