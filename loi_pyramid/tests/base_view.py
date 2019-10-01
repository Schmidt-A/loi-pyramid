# flake8: noqa
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPClientError
from pyramid import testing

from .base_test import BaseTest
from ..views import BaseView
from ..models import Account, Character, Action

log = logging.getLogger(__name__)


class TestBaseViews(BaseTest):

    # Initial setup for these tests
    # Needs to be broken up
    def setUp(self):
        super(TestBaseViews, self).setUp()
        self.init_database()

        accounts_data = self.fixture_helper.account_data()
        characters_data = self.fixture_helper.character_data()
        actions_data = self.fixture_helper.action_data()
        self.session.flush()

        self.accounts = self.fixture_helper.convert_to_json(accounts_data)
        self.characters = self.fixture_helper.convert_to_json(characters_data)
        self.actions = self.fixture_helper.convert_to_json(actions_data)

        self.fake_accounts = self.fixture_helper.fake_account_fixture()

    def mock_get(self, first, user_account):
        resources = [('accounts', ('username', first['username']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            account=user_account)

        mock_view = BaseView(testing.DummyResource(), request)

        return mock_view.get_one(Account).json_body

    def mock_get_all(self, user_account, limit=None, offset=None):
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

        mock_view = BaseView(testing.DummyResource(), request)

        return mock_view.get_all(Account).json_body

    def mock_get_all_by(self, first, user_account, limit=None, offset=None):
        resources = [
            ('accounts', ('username', first['username'])),
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

        mock_view = BaseView(testing.DummyResource(), request)

        return mock_view.get_all_by_one(Account, Character).json_body

    def mock_get_one_by(self, first, second, user_account):
        resources = [
            ('characters', ('charId', first['id'])),
            ('actions', ('actionId', second['id']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            account=user_account)

        mock_view = BaseView(testing.DummyResource(), request)

        return mock_view.get_one_by_one(Character, Action).json_body

    # TODO: Make these tests more generic

    # Test that we can get Tweek via get call
    def test_get(self):
        account_result = self.mock_get(
            self.accounts['tweek'],
            self.accounts['tweek'])

        self.assert_compare_objects(account_result, self.accounts['tweek'], 
            *Account.__owned__(Account))

    # Test that we can only see public Tweek via get call
    def test_get_public(self):
        account_result = self.mock_get(
            self.accounts['tweek'], self.accounts['noob'])

        self.assert_compare_objects(account_result, self.accounts['tweek'], 
            *Account.__public__(Account))

        self.assert_not_in_object(account_result, *Account.__private__(Account))

    # Test that we cannot get Tam via get call
    # Because he'll never nut up and log on
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.mock_get(self.fake_accounts['tam'], self.accounts['tweek'])

    # Test that we can get all accounts via get all call without limit

    def test_get_all(self):
        total = 10
        offset = 0
        accounts_result = self.mock_get_all(self.accounts['tweek'])

        compare_accounts = list(self.accounts.values())[offset:offset + total]
        
        self.assertEqual(
            accounts_result['offset'],
            offset + len(compare_accounts))

        total_accounts = len(list(self.accounts.values()))
        self.assertEqual(accounts_result['total'], total_accounts)

        self.assert_compare_lists(accounts_result['accounts'], compare_accounts,
             *Account.__owned__(Account))

    # Test that we can get all accounts via get all call with limit 2 offset 0
    def test_get_all_1st(self):
        total = 1
        offset = 0
        accounts_result = self.mock_get_all(
            self.accounts['tweek'], total, offset)

        compare_accounts = list(self.accounts.values())[offset:offset + total]
        self.assertEqual(
            accounts_result['offset'],
            offset + len(compare_accounts))

        total_accounts = len(list(self.accounts.values()))
        self.assertEqual(accounts_result['total'], total_accounts)

        self.assert_compare_lists(accounts_result['accounts'], compare_accounts,
             *Account.__owned__(Account))

    # Test that we can get all accounts via get all call with limit 2 offset 2
    def test_get_all_2nd(self):
        total = 1
        offset = 1
        accounts_result = self.mock_get_all(
            self.accounts['tweek'], total, offset)

        compare_accounts = list(self.accounts.values())[offset:offset + total]
        self.assertEqual(
            accounts_result['offset'],
            offset + len(compare_accounts))

        total_accounts = len(list(self.accounts.values()))
        self.assertEqual(accounts_result['total'], total_accounts)

        self.assert_compare_lists(accounts_result['accounts'], compare_accounts,
             *Account.__owned__(Account))

    # Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_admin(self):
        total = 10
        offset = 0
        characters_result = self.mock_get_all_by(
            self.accounts['noob'], self.accounts['tweek'])

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['noob']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset + total]

        self.assertEqual(
            characters_result['offset'],
            offset + len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        self.assert_compare_lists(characters_result['characters'], compare_characters,
             *Character.__owned__(Character))

    # Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_admin_1st(self):
        total = 1
        offset = 0
        characters_result = self.mock_get_all_by(
            self.accounts['noob'], self.accounts['tweek'], total, offset)

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['noob']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset + total]

        self.assertEqual(
            characters_result['offset'],
            offset + len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        self.assert_compare_lists(characters_result['characters'], compare_characters,
             *Character.__owned__(Character))

    # Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_admin_2nd(self):
        total = 1
        offset = 1
        characters_result = self.mock_get_all_by(
            self.accounts['noob'], self.accounts['tweek'], total, offset)

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['noob']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset + total]

        self.assertEqual(
            characters_result['offset'],
            offset + len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        self.assert_compare_lists(characters_result['characters'], compare_characters,
             *Character.__owned__(Character))

    # Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_owned(self):
        total = 10
        offset = 0
        characters_result = self.mock_get_all_by(
            self.accounts['noob'], self.accounts['noob'])

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['noob']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset + total]

        self.assertEqual(
            characters_result['offset'],
            offset + len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        self.assert_compare_lists(characters_result['characters'], compare_characters,
             *Character.__owned__(Character))

    # Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_public(self):
        total = 10
        offset = 0
        characters_result = self.mock_get_all_by(
            self.accounts['tweek'], self.accounts['noob'])

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['tweek']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset + total]

        self.assertEqual(
            characters_result['offset'],
            offset + len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        self.assert_compare_lists(characters_result['characters'], compare_characters,
             *Character.__public__(Character))

        for character in characters_result['characters']:
            self.assert_not_in_object(character, *Character.__private__(Character))

    # Test that we can get the Jilin's training via get call when owner
    # Because the noob account owns jilin

    def test_get_one_by_one_owned(self):
        train = self.mock_get_one_by(
            self.characters['jilin'],
            self.actions['noob_train'],
            self.accounts['noob'])

        self.assertEqual(train['characterId'], self.characters['jilin']['id'])

        self.assert_compare_objects(train, self.actions['noob_train'], 
            *Action.__public__(Action))

    # Test that we cannot get Al's crafting via get call when not owner
    # Because the noob account doesn't own alrunden
    def test_get_one_by_one_not_owned(self):
        with self.assertRaises(HTTPForbidden):
            self.mock_get_one_by(
                self.characters['alrunden'],
                self.actions['al_craft'],
                self.accounts['noob'])

    # Test that we can see the Jilin's mining via get call when admin
    # Because admins can access any character
    def test_get_one_by_one_admin(self):
        mining = self.mock_get_one_by(
            self.characters['jilin'],
            self.actions['noob_mine'],
            self.accounts['aez'])

        self.assertEqual(mining['characterId'], self.characters['jilin']['id'])
        
        self.assert_compare_objects(mining, self.actions['noob_mine'], 
            *Action.__public__(Action))
