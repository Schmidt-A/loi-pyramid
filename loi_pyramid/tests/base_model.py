import logging

from pyramid import testing

from .base_test import BaseTest
from ..models import Account, Character, Action, Recipe

log = logging.getLogger(__name__)


class TestBaseModels(BaseTest):

    # Initial setup for these tests
    # Needs to be broken up
    def setUp(self):
        super(TestBaseModels, self).setUp()
        self.init_database()

        self.accounts = self.fixture_helper.account_data()
        self.characters = self.fixture_helper.character_data()
        self.actions = self.fixture_helper.action_data()

        self.session.flush()

    def test_model_fk(self):
        foreign_key = Character.get_foreign_key_by(Character, Account)

        self.assertEqual(foreign_key.column.name, 'username')
        self.assertEqual(foreign_key.column.table.name, 'accounts')
        self.assertEqual(foreign_key.parent.name, 'accountId')

    def test_instance_fk(self):
        account = self.accounts['tweek']
        character = self.characters['siobhan']

        foreign_key = character.get_foreign_key_by(Account)

        self.assertEqual(foreign_key.column.name, 'username')
        self.assertEqual(foreign_key.column.table.name, 'accounts')
        self.assertEqual(foreign_key.parent.name, 'accountId')

    def test_model_no_fk(self):
        foreign_key = Account.get_foreign_key_by(Account, Character)

        self.assertEqual(foreign_key, None)

    def test_instance_no_fk(self):
        account = self.accounts['tweek']

        foreign_key = account.get_foreign_key_by(Character)

        self.assertEqual(foreign_key, None)

    def test_model_multiple_fk(self):
        first_foreign_key = Action.get_foreign_key_by(Action, Character)

        self.assertEqual(first_foreign_key.column.name, 'id')
        self.assertEqual(first_foreign_key.column.table.name, 'characters')
        self.assertEqual(first_foreign_key.parent.name, 'characterId')

        second_foreign_key = Action.get_foreign_key_by(Action, Recipe)

        self.assertEqual(second_foreign_key.column.name, 'blueprint')
        self.assertEqual(second_foreign_key.column.table.name, 'recipes')
        self.assertEqual(second_foreign_key.parent.name, 'blueprint')

    def test_instance_multiple_fk(self):
        action = self.actions['al_craft']

        first_foreign_key = action.get_foreign_key_by(Character)

        self.assertEqual(first_foreign_key.column.name, 'id')
        self.assertEqual(first_foreign_key.column.table.name, 'characters')
        self.assertEqual(first_foreign_key.parent.name, 'characterId')

        second_foreign_key = action.get_foreign_key_by(Recipe)

        self.assertEqual(second_foreign_key.column.name, 'blueprint')
        self.assertEqual(second_foreign_key.column.table.name, 'recipes')
        self.assertEqual(second_foreign_key.parent.name, 'blueprint')
