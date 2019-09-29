# flake8: noqa
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPClientError
from pyramid import testing

from .base_test import BaseTest
from ..views import BaseView
from ..models import Account, Character, Action

log = logging.getLogger(__name__)

class TestBaseViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestBaseViews, self).setUp()
        self.init_database()

        self.accounts = self.fixture_helper.account_fixture()
        self.characters = self.fixture_helper.character_fixture()
        self.actions = self.fixture_helper.action_fixture()
        self.session.flush()

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
        if limit != None:
            query['limit'] = limit
        if offset != None:
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
        if limit != None:
            query['limit'] = limit
        if offset != None:
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

    #TODO: Make these tests more generic

    #Test that we can get Tweek via get call
    def test_get(self):
        account_result = self.mock_get(self.accounts['tweek'], self.accounts['tweek'])

        self.assertEqual(account_result['username'], self.accounts['tweek']['username'])
        self.assertEqual(account_result['cdkey'], self.accounts['tweek']['cdkey'])
        self.assertEqual(account_result['role'], self.accounts['tweek']['role'])
        self.assertEqual(account_result['approved'], self.accounts['tweek']['approved'])
        self.assertEqual(account_result['banned'], self.accounts['tweek']['banned'])
        self.assertEqual(account_result['created'], self.accounts['tweek']['created'])
        self.assertEqual(account_result['updated'], self.accounts['tweek']['updated'])

    #Test that we can only see public Tweek via get call
    def test_get_public(self):
        account_result = self.mock_get(self.accounts['tweek'], self.accounts['noob'])

        self.assertEqual(account_result['username'], self.accounts['tweek']['username'])
        self.assertEqual(account_result['role'], self.accounts['tweek']['role'])
        self.assertEqual(account_result['approved'], self.accounts['tweek']['approved'])
        self.assertEqual(account_result['banned'], self.accounts['tweek']['banned'])
        self.assertEqual(account_result['created'], self.accounts['tweek']['created'])
        self.assertEqual(account_result['updated'], self.accounts['tweek']['updated'])

        with self.assertRaises(KeyError):
            account_result['cdkey']
        with self.assertRaises(KeyError):
            account_result['ip']

    #Test that we cannot get Tam via get call
    #Because he'll never nut up and log on
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.mock_get(self.fake_accounts['tam'], self.accounts['tweek'])


    #Test that we can get all accounts via get all call without limit
    def test_get_all(self):
        total = 10
        offset = 0
        accounts_result = self.mock_get_all(self.accounts['tweek'])

        compare_accounts = list(self.accounts.values())[offset:offset+total]
        self.assertEqual(len(accounts_result['accounts']), len(compare_accounts))
        self.assertEqual(accounts_result['offset'], offset+len(compare_accounts))

        total_accounts = len(list(self.accounts.values()))
        self.assertEqual(accounts_result['total'], total_accounts)

        for account, compare_account in zip(accounts_result['accounts'], compare_accounts):
            self.assertEqual(account['username'], compare_account['username'])
            self.assertEqual(account['cdkey'], compare_account['cdkey'])
            self.assertEqual(account['role'], compare_account['role'])
            self.assertEqual(account['approved'], compare_account['approved'])
            self.assertEqual(account['banned'], compare_account['banned'])
            self.assertEqual(account['created'], compare_account['created'])
            self.assertEqual(account['updated'], compare_account['updated'])

    #Test that we can get all accounts via get all call with limit 2 offset 0
    def test_get_all_1st(self):
        total = 1
        offset = 0
        accounts_result = self.mock_get_all(self.accounts['tweek'], total, offset)

        compare_accounts = list(self.accounts.values())[offset:offset+total]
        self.assertEqual(len(accounts_result['accounts']), len(compare_accounts))
        self.assertEqual(accounts_result['offset'], offset+len(compare_accounts))

        total_accounts = len(list(self.accounts.values()))
        self.assertEqual(accounts_result['total'], total_accounts)

        for account, compare_account in zip(accounts_result['accounts'], compare_accounts):
            self.assertEqual(account['username'], compare_account['username'])
            self.assertEqual(account['cdkey'], compare_account['cdkey'])
            self.assertEqual(account['role'], compare_account['role'])
            self.assertEqual(account['approved'], compare_account['approved'])
            self.assertEqual(account['banned'], compare_account['banned'])
            self.assertEqual(account['created'], compare_account['created'])
            self.assertEqual(account['updated'], compare_account['updated'])

    #Test that we can get all accounts via get all call with limit 2 offset 2
    def test_get_all_2nd(self):
        total = 1
        offset = 1
        accounts_result = self.mock_get_all(self.accounts['tweek'], total, offset)

        compare_accounts = list(self.accounts.values())[offset:offset+total]
        self.assertEqual(len(accounts_result['accounts']), len(compare_accounts))
        self.assertEqual(accounts_result['offset'], offset+len(compare_accounts))

        total_accounts = len(list(self.accounts.values()))
        self.assertEqual(accounts_result['total'], total_accounts)

        for account, compare_account in zip(accounts_result['accounts'], compare_accounts):
            self.assertEqual(account['username'], compare_account['username'])
            self.assertEqual(account['cdkey'], compare_account['cdkey'])
            self.assertEqual(account['role'], compare_account['role'])
            self.assertEqual(account['approved'], compare_account['approved'])
            self.assertEqual(account['banned'], compare_account['banned'])
            self.assertEqual(account['created'], compare_account['created'])
            self.assertEqual(account['updated'], compare_account['updated'])

    #Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_admin(self):
        total = 10
        offset = 0
        characters_result = self.mock_get_all_by(self.accounts['noob'], self.accounts['tweek'])

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['noob']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset+total]

        self.assertEqual(len(characters_result['characters']), len(compare_characters))
        self.assertEqual(characters_result['offset'], offset+len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        for character, compare_character in zip(characters_result['characters'], compare_characters):
            self.assertEqual(character['accountId'], compare_character['accountId'])
            self.assertEqual(character['name'], compare_character['name'])
            self.assertEqual(character['exp'], compare_character['exp'])
            self.assertEqual(character['area'], compare_character['area'])
            self.assertEqual(character['created'], compare_character['created'])
            self.assertEqual(character['updated'], compare_character['updated'])

    #Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_admin_1st(self):
        total = 1
        offset = 0
        characters_result = self.mock_get_all_by(self.accounts['noob'], self.accounts['tweek'], total, offset)

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['noob']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset+total]

        self.assertEqual(len(characters_result['characters']), len(compare_characters))
        self.assertEqual(characters_result['offset'], offset+len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        for character, compare_character in zip(characters_result['characters'], compare_characters):
            self.assertEqual(character['accountId'], compare_character['accountId'])
            self.assertEqual(character['name'], compare_character['name'])
            self.assertEqual(character['exp'], compare_character['exp'])
            self.assertEqual(character['area'], compare_character['area'])
            self.assertEqual(character['created'], compare_character['created'])
            self.assertEqual(character['updated'], compare_character['updated'])

    #Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_admin_2nd(self):
        total = 1
        offset = 1
        characters_result = self.mock_get_all_by(self.accounts['noob'], self.accounts['tweek'], total, offset)

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['noob']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset+total]

        self.assertEqual(len(characters_result['characters']), len(compare_characters))
        self.assertEqual(characters_result['offset'], offset+len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        for character, compare_character in zip(characters_result['characters'], compare_characters):
            self.assertEqual(character['accountId'], compare_character['accountId'])
            self.assertEqual(character['name'], compare_character['name'])
            self.assertEqual(character['exp'], compare_character['exp'])
            self.assertEqual(character['area'], compare_character['area'])
            self.assertEqual(character['created'], compare_character['created'])
            self.assertEqual(character['updated'], compare_character['updated'])

    #Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_owned(self):
        total = 10
        offset = 0
        characters_result = self.mock_get_all_by(self.accounts['noob'], self.accounts['noob'])

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['noob']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset+total]

        self.assertEqual(len(characters_result['characters']), len(compare_characters))
        self.assertEqual(characters_result['offset'], offset+len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        for character, compare_character in zip(characters_result['characters'], compare_characters):
            self.assertEqual(character['accountId'], compare_character['accountId'])
            self.assertEqual(character['name'], compare_character['name'])
            self.assertEqual(character['exp'], compare_character['exp'])
            self.assertEqual(character['area'], compare_character['area'])
            self.assertEqual(character['created'], compare_character['created'])
            self.assertEqual(character['updated'], compare_character['updated'])

    #Test that we can get all characters for Tweek via get all call
    def test_get_all_by_one_public(self):
        total = 10
        offset = 0
        characters_result = self.mock_get_all_by(self.accounts['tweek'], self.accounts['noob'])

        owned_characters = []
        for key, char in self.characters.items():
            if char['accountId'] == self.accounts['tweek']['username']:
                owned_characters.append(char)

        compare_characters = owned_characters[offset:offset+total]

        self.assertEqual(len(characters_result['characters']), len(compare_characters))
        self.assertEqual(characters_result['offset'], offset+len(compare_characters))

        total_characters = len(owned_characters)
        self.assertEqual(characters_result['total'], total_characters)

        for character, compare_character in zip(characters_result['characters'], compare_characters):
            self.assertEqual(character['accountId'], compare_character['accountId'])
            self.assertEqual(character['name'], compare_character['name'])
            self.assertEqual(character['created'], compare_character['created'])
            self.assertEqual(character['updated'], compare_character['updated'])

            with self.assertRaises(KeyError):
                character['exp']
            with self.assertRaises(KeyError):
                character['area']


    #Test that we can get the Jilin's training via get call when owner
    #Because the noob account owns jilin
    def test_get_one_by_one_owned(self):
        train = self.mock_get_one_by(self.characters['jilin'], self.actions['noob_train'], self.accounts['noob'])

        self.assertEqual(train['characterId'], self.characters['jilin']['id'])
        self.assertEqual(train['resref'], self.actions['noob_train']['resref'])
        self.assertEqual(train['amount'], self.actions['noob_train']['amount'])
        self.assertEqual(train['blueprint'], self.actions['noob_train']['blueprint'])
        self.assertEqual(train['ingredients'], self.actions['noob_train']['ingredients'])
        self.assertEqual(train['completed'], self.actions['noob_train']['completed'])

    #Test that we cannot get Al's crafting via get call when not owner
    #Because the noob account doesn't own alrunden
    def test_get_one_by_one_not_owned(self):
        with self.assertRaises(HTTPForbidden):
            self.mock_get_one_by(self.characters['alrunden'], self.actions['al_craft'], self.accounts['noob'])

    #Test that we can see the Jilin's mining via get call when admin
    #Because admins can access any character
    def test_get_one_by_one_admin(self):
        mining = self.mock_get_one_by(self.characters['jilin'], self.actions['noob_mine'], self.accounts['aez'])

        self.assertEqual(mining['characterId'], self.characters['jilin']['id'])
        self.assertEqual(mining['resref'], self.actions['noob_mine']['resref'])
        self.assertEqual(mining['amount'], self.actions['noob_mine']['amount'])
        self.assertEqual(mining['blueprint'], self.actions['noob_mine']['blueprint'])
        self.assertEqual(mining['ingredients'], self.actions['noob_mine']['ingredients'])
        self.assertEqual(mining['completed'], self.actions['noob_mine']['completed'])
