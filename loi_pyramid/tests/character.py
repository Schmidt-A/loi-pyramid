# flake8: noqa
import logging
import copy

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPClientError
from pyramid import testing

from .base_test import BaseTest
from ..views.character import CharacterViews, CharactersViews, CharacterItemsViews, CharacterItemViews
from ..views.character import CharacterActionViews, CharacterActionsViews
from ..models import Character, Item, Action

log = logging.getLogger(__name__)


class TestCharacterViews(BaseTest):

    # Initial setup for these tests
    # Needs to be broken up
    def setUp(self):
        super(TestCharacterViews, self).setUp()
        self.init_database()

        accounts_data = self.fixture_helper.account_data()
        characters_data = self.fixture_helper.character_data()
        items_data = self.fixture_helper.item_data()
        actions_data = self.fixture_helper.action_data()
        self.session.flush()

        self.accounts = self.fixture_helper.convert_to_json(accounts_data)
        self.characters = self.fixture_helper.convert_to_json(characters_data)
        self.items = self.fixture_helper.convert_to_json(items_data)
        self.actions = self.fixture_helper.convert_to_json(actions_data)

        self.fake_characters = self.fixture_helper.fake_character_fixture()
        self.fake_accounts = self.fixture_helper.fake_account_fixture()
        self.fake_items = self.fixture_helper.fake_item_fixture()
        self.fake_actions = self.fixture_helper.fake_action_fixture()

    # Helper method for get calls to /characters/{id}
    def character_get(self, character, account):
        resources = [('characters', ('charId', character['id']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            account=account)

        char_view = CharacterViews(testing.DummyResource(), request)

        return char_view.get().json_body

    # Helper method for delete calls to /characters/{id}
    def character_delete(self, character, account):
        resources = [('characters', ('charId', character['id']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            method='DELETE',
            account=account)

        char_view = CharacterViews(testing.DummyResource(), request)

        return char_view.delete().json_body

    # Helper method for update calls to /characters/{id}
    def character_update(self, character, account):
        resources = [('characters', ('charId', character['id']))]

        character_payload = {
            'accountId': character['accountId'],
            'name': character['name'],
            'exp': character['exp'],
            'area': character['area'],
        }

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            method='PUT',
            body=character_payload,
            account=account)

        char_view = CharacterViews(testing.DummyResource(), request)

        return char_view.update().json_body

    # Helper method for get all calls to /characters
    def characters_get_all(self, account, limit=None, offset=None):
        resources = [('characters', ('charId', ''))]

        query = {}
        if limit is not None:
            query['limit'] = limit
        if offset is not None:
            query['offset'] = offset

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            query=query,
            account=account)

        char_view = CharactersViews(testing.DummyResource(), request)

        return char_view.get().json_body

    # Helper method for get calls for /characters/{id}/items/{id}
    def item_get(self, character, item, account):
        resources = [
            ('characters', ('charId', character['id'])),
            ('items', ('itemId', item['id']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            account=account)

        char_view = CharacterItemViews(testing.DummyResource(), request)

        return char_view.get().json_body

    # Helper method for update calls for /characters/{id}/items/{id}
    def item_update(self, character, item, account):
        resources = [
            ('characters', ('charId', character['id'])),
            ('items', ('itemId', item['id']))]

        item_payload = {
            'resref': item['resref'],
            'amount': item['amount']
        }

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            method='PUT',
            body=item_payload,
            account=account)

        char_view = CharacterItemViews(testing.DummyResource(), request)

        return char_view.update().json_body

    # Helper method for delete calls for /characters/{id}/items/{id}
    def item_delete(self, character, item, account):
        resources = [
            ('characters', ('charId', character['id'])),
            ('items', ('itemId', item['id']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            method='DELETE',
            account=account)

        char_view = CharacterItemViews(testing.DummyResource(), request)

        return char_view.delete().json_body

    # Helper method for get all calls to /characters/{id}/items
    def items_get_all(self, character, account, limit=None, offset=None):
        resources = [
            ('characters', ('charId', character['id'])),
            ('items', ('itemId', ''))]

        query = {}
        if limit is not None:
            query['limit'] = limit
        if offset is not None:
            query['offset'] = offset

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            query=query,
            account=account)

        char_view = CharacterItemsViews(testing.DummyResource(), request)

        return char_view.get().json_body

    # Helper method for create calls to /characters/{id}/items
    def items_create(self, character, item, account):
        resources = [
            ('characters', ('charId', character['id'])),
            ('items', ('itemId', ''))]

        item_payload = {
            'characterId': item['characterId'],
            'resref': item['resref'],
            'amount': item['amount']
        }

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            method='POST',
            body=item_payload,
            account=account)

        char_view = CharacterItemsViews(testing.DummyResource(), request)

        return char_view.create().json_body

    # Helper method for get calls for /characters/{id}/actions/{id}
    def action_get(self, character, action, account):
        resources = [
            ('characters', ('charId', character['id'])),
            ('actions', ('actionId', action['id']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            account=account)

        char_view = CharacterActionViews(testing.DummyResource(), request)

        return char_view.get().json_body

    # Helper method for get all calls to /characters/{id}/actions
    def actions_get_all(self, character, account, limit=None, offset=None):
        resources = [
            ('characters', ('charId', character['id'])),
            ('actions', ('actionId', ''))]

        query = {}
        if limit is not None:
            query['limit'] = limit
        if offset is not None:
            query['offset'] = offset

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            query=query,
            account=account)

        char_view = CharacterActionsViews(testing.DummyResource(), request)

        return char_view.get().json_body

    # Helper method for delete calls for /characters/{id}/actions/{id}
    def action_delete(self, character, action, account):
        resources = [
            ('characters', ('charId', character['id'])),
            ('actions', ('actionId', action['id']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            method='DELETE',
            account=account)

        char_view = CharacterActionViews(testing.DummyResource(), request)

        return char_view.delete().json_body

    # Helper method for create calls to /characters/{id}/actions
    def actions_create(self, character, action, account):
        resources = [
            ('characters', ('charId', character['id'])),
            ('actions', ('actionId', ''))]

        action_payload = {
            'amount': action['amount'],
            'blueprint': action['blueprint']
        }

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            method='POST',
            account=account)

        char_view = CharacterActionsViews(testing.DummyResource(), request)

        return char_view.create().json_body

    # Test that we can get Ji'Lin via get call when owner
    # Because noob owns Ji'Lin
    def test_owner_get_char(self):
        character_result = self.character_get(
            self.characters['jilin'], self.accounts['noob'])

        self.assert_compare_objects(character_result, self.characters['jilin'], 
            *Character.__owned__(Character))

    # Test that we cannot get Siobhan via get call when not owner
    # Because noob doesnt own Siobhan
    def test_not_owner_get_char(self):
        character_result = self.character_get(
            self.characters.get('siobhan'), self.accounts['noob'])

        self.assert_compare_objects(character_result, self.characters['siobhan'], 
            *Character.__public__(Character))
        self.assert_not_in_object(character_result, *Character.__private__(Character))

    # Test that we can get Ji'Lin via get call when admin
    # Because admins can look at other peoples' chars
    def test_admin_get_char(self):
        character_result = self.character_get(
            self.characters['jilin'], self.accounts['tweek'])

        self.assert_compare_objects(character_result, self.characters['jilin'], 
            *Character.__owned__(Character))

    # Test that we cannot get Meero via get call when admin
    # Because she ain't created
    def test_admin_get_char_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.character_get(
                self.fake_characters['meero'],
                self.accounts['tweek'])

    # Test that we can update Siobhan's name via put call when admin
    # She got some rp exp
    def test_admin_update_char(self):
        test_spy = copy.copy(self.characters.get('siobhan'))
        test_spy['exp'] = 11000

        character_result = self.character_update(
            test_spy, self.accounts['tweek'])

        self.assertEqual(character_result['accountId'], test_spy['accountId'])
        self.assertEqual(character_result['name'], test_spy['name'])
        self.assertEqual(character_result['exp'], test_spy['exp'])
        self.assertEqual(character_result['area'], test_spy['area'])
        self.assertEqual(character_result['created'], test_spy['created'])
        # TODO: Need update test for updated timestamp

    # Test that we cannot update Meero's name via get call when admin
    # Because she ain't created
    def test_admin_update_char_not_found(self):
        test_slave = copy.copy(self.fake_characters['meero'])
        test_slave['exp'] = 5000

        with self.assertRaises(HTTPNotFound):
            self.character_update(test_slave, self.accounts['tweek'])

    # Test that we cannot update Jilin's name via put call when not admin
    # Because only admins can do that
    def test_not_admin_update_char(self):
        test_drow = copy.copy(self.characters['jilin'])
        test_drow['exp'] = 99999999

        with self.assertRaises(HTTPForbidden):
            self.character_update(test_drow, self.accounts['noob'])

        # Should we test that the info wasn't altered afterwards?

    # Test that we can delete Arthen via delete call when admin
    # Test that he isn't available via get afterwards
    def test_admin_delete_char(self):
        characters_result = self.character_delete(
            self.characters['arthen'], self.accounts['tweek'])
        
        remaining_total = len(self.characters.keys())-1
        return_total = remaining_total if remaining_total < 10 else 10

        self.assertEqual(characters_result['total'], remaining_total)
        self.assertEqual(
            len(characters_result['characters']), return_total)
        with self.assertRaises(HTTPNotFound):
            self.character_get(
                self.characters['arthen'],
                self.accounts['tweek'])

    # Test that we cannot delete Meero when admin
    # Because she ain't created
    def test_admin_delete_char_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.character_delete(
                self.fake_characters['meero'],
                self.accounts['tweek'])

    # Test that we cannot delete Jilin via delete call when not admin
    # Because only admins can do that
    def test_not_admin_delete_char(self):
        with self.assertRaises(HTTPForbidden):
            self.character_delete(
                self.characters['jilin'],
                self.accounts['noob'])

        # Should we test that the info wasn't altered afterwards?

    # Test that we can get all characters via get all call when admin
    # And that we get the full info payload
    # Because only admins and owners get full payload
    def test_admin_get_all_char(self):
        total = 10
        offset = 0
        characters_result = self.characters_get_all(self.accounts['tweek'])

        compare_characters = list(self.characters.values())[
            offset:offset + total]
        self.assertEqual(
            len(characters_result['characters']), len(compare_characters))
        self.assertEqual(
            characters_result['offset'],
            offset + len(compare_characters))

        total_characters = len(list(self.characters.values()))
        self.assertEqual(characters_result['total'], total_characters)

        for char, compare_char in zip(
                characters_result['characters'], compare_characters):
            self.assert_compare_objects(char, compare_char, 
                *Character.__owned__(Character))

    # Test that we can get all characters via get all call when not admin
    # And that we get the partial info payload
    # Because only admins and owners get full payload
    def test_not_admin_get_all_char(self):
        total = 10
        offset = 0
        characters_result = self.characters_get_all(self.accounts['noob'])

        compare_characters = list(self.characters.values())[
            offset:offset + total]
        self.assertEqual(
            len(characters_result['characters']), len(compare_characters))
        self.assertEqual(
            characters_result['offset'],
            offset + len(compare_characters))

        total_characters = len(list(self.characters.values()))
        self.assertEqual(characters_result['total'], total_characters)

        for char, compare_char in zip(
                characters_result['characters'], compare_characters):
            self.assert_compare_objects(char, compare_char, 
                *Character.__public__(Character))
            self.assert_not_in_object(char, *Character.__private__(Character))

    # Test that we can get the Jilin's money via get call when owner
    # Because the noob account owns jilin
    def test_own_get_item(self):
        item_result = self.item_get(
            self.characters['jilin'],
            self.items['noob_money'],
            self.accounts['noob'])

        self.assert_compare_objects(item_result, self.items['noob_money'], 
            *Item.__owned__(Item))

    # Test that we cannot get the Al's money via get call when not owner
    # Because the noob account doesn't own alrunden
    def test_not_own_get_item(self):
        with self.assertRaises(HTTPForbidden):
            self.item_get(
                self.characters['alrunden'],
                self.items['al_money'],
                self.accounts['noob'])

    # Test that we can get the Jilin's money via get call when admin
    # Because admins can access any character
    def test_admin_get_item(self):
        item_result = self.item_get(
            self.characters['jilin'],
            self.items['noob_money'],
            self.accounts['aez'])

        self.assert_compare_objects(item_result, self.items['noob_money'], 
            *Item.__owned__(Item))

    # Test that we cannot get Al's cows with Siobhan's id via get call when admin
    # Because those are owned by Al's character, not Siobhan's
    def test_admin_get_item_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.item_get(
                self.characters.get('siobhan'),
                self.items['al_cow'],
                self.accounts['aez'])

    # Test that we cannot get Al's Zombie via get call when admin
    # Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_get_item_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_get(
                self.characters['alrunden'],
                self.fake_items['al_zombie'],
                self.accounts['aez'])

    # Test that we can increase Al's money via put call when admin
    def test_admin_update_item(self):
        test_money = copy.copy(self.items['al_money'])
        test_money['amount'] = 200000
        item_result = self.item_update(
            self.characters['alrunden'],
            test_money,
            self.accounts['aez'])

        self.assertEqual(item_result['characterId'], test_money['characterId'])
        self.assertEqual(item_result['resref'], test_money['resref'])
        self.assertEqual(item_result['amount'], test_money['amount'])
        self.assertEqual(item_result['created'], test_money['created'])
        self.assertGreater(item_result['updated'], test_money['updated'])

    # Test that we cannot update Al's cows with Siobhan's id via put call when admin
    # Because those are owned by Al's character, not Siobhan's
    def test_admin_update_item_not_assoc(self):
        test_cow = copy.copy(self.items['al_cow'])
        test_cow['amount'] = 9

        with self.assertRaises(HTTPClientError):
            self.item_update(
                self.characters.get('siobhan'),
                test_cow,
                self.accounts['aez'])

    # Test that we cannot update Al's Zombie count via put call when admin
    # Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_update_item_not_found(self):
        test_zombie = copy.copy(self.fake_items['al_zombie'])
        test_zombie['amount'] = 5

        with self.assertRaises(HTTPNotFound):
            self.item_update(
                self.characters['alrunden'],
                test_zombie,
                self.accounts['aez'])

    # Test that we cannot update Jilin's money when not admin
    # Because only admins can do that
    def test_not_admin_update_item(self):
        test_money = copy.copy(self.items['noob_money'])
        test_money['amount'] = 45000

        with self.assertRaises(HTTPForbidden):
            self.item_update(
                self.characters['jilin'],
                test_money,
                self.accounts['noob'])

    # Test that we can remove cows and sheep from Al's items via delete call when admin
    # Test that Cows and Sheeps are not accessible via get call
    # Because Al's farm got stolen from
    def test_admin_delete_item(self):
        #not giving this a variable because we don't need to see the result twice
        self.item_delete(
            self.characters['alrunden'],
            self.items['al_cow'],
            self.accounts['aez'])
        items_result = self.item_delete(
            self.characters['alrunden'],
            self.items['al_sheep'],
            self.accounts['aez'])

        compare_items = []
        for key, item in self.items.items():
            if item['characterId'] == self.characters['alrunden']['id']:
                compare_items.append(item)

        remaining_total = len(compare_items)-2
        return_total = remaining_total if remaining_total < 10 else 10

        self.assertEqual(items_result['total'], remaining_total)
        self.assertEqual(
            len(items_result['items']), return_total)
        with self.assertRaises(HTTPNotFound):
            self.item_get(
                self.characters['alrunden'],
                self.items['al_cow'],
                self.accounts['aez'])
        with self.assertRaises(HTTPNotFound):
            self.item_get(
                self.characters['alrunden'],
                self.items['al_sheep'],
                self.accounts['aez'])

    # Test that we cannot delete Al's cows with Siobhan's id via get call when admin
    # Because those are owned by Al's character, not Siobhan's
    def test_admin_delete_item_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.item_delete(
                self.characters.get('siobhan'),
                self.items['al_cow'],
                self.accounts['aez'])

    # Test that we cannot get Al's Zombie via delete call when admin
    # Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_delete_item_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_delete(
                self.characters['alrunden'],
                self.fake_items['al_zombie'],
                self.accounts['aez'])

    # Test that we cannot remove cows from Al's items via delete call when not admin
    # Because only admins can do that
    def test_not_admin_delete_item(self):
        with self.assertRaises(HTTPForbidden):
            self.item_delete(
                self.characters['alrunden'],
                self.items['al_cow'],
                self.accounts['noob'])

    # Test that we can get Jilin's items via get all call when owner
    def test_own_get_all_item(self):
        total = 10
        offset = 0
        items_result = self.items_get_all(
            self.characters['jilin'], self.accounts['noob'])

        owned_items = []
        for key, item in self.items.items():
            if item['characterId'] == self.characters['jilin']['id']:
                owned_items.append(item)

        compare_items = owned_items[offset:offset + total]
        self.assertEqual(len(items_result['items']), len(compare_items))
        self.assertEqual(items_result['offset'], offset + len(compare_items))

        total_items = len(owned_items)
        self.assertEqual(items_result['total'], total_items)

        for item, compare_item in zip(items_result['items'], compare_items):
            self.assert_compare_objects(item, compare_item, 
                *Item.__owned__(Item))

    # Test that we can't get Al's items via get all call when not owner
    # Because you can't see other people's shit
    def test_not_own_get_all_item(self):
        with self.assertRaises(HTTPForbidden):
            self.items_get_all(
                self.characters['alrunden'],
                self.accounts['noob'])

    # Test that we can get Jilin's items via get all call when admin
    # Because admins can see everything
    def test_admin_get_all_item(self):
        total = 10
        offset = 0
        items_result = self.items_get_all(
            self.characters['jilin'], self.accounts['aez'])

        owned_items = []
        for key, item in self.items.items():
            if item['characterId'] == self.characters['jilin']['id']:
                owned_items.append(item)

        compare_items = owned_items[offset:offset + total]
        self.assertEqual(len(items_result['items']), len(compare_items))
        self.assertEqual(items_result['offset'], offset + len(compare_items))

        total_items = len(owned_items)
        self.assertEqual(items_result['total'], total_items)

        for item, compare_item in zip(items_result['items'], compare_items):
            self.assert_compare_objects(item, compare_item, 
                *Item.__owned__(Item))

    # Test that we cannot get Meero's items via get all call when admin
    # Because she ain't created
    def test_admin_get_all_items_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.items_get_all(
                self.fake_characters['meero'],
                self.accounts['aez'])

    # Test that we can create a new armor on Al via post call when admin
    # Because Viti's campaign is ridiculous with loot
    def test_admin_create_item(self):
        item_result = self.items_create(
            self.characters['alrunden'],
            self.fake_items['op_armor'],
            self.accounts['aez'])

        self.assertEqual(
            item_result['characterId'],
            self.fake_items['op_armor']['characterId'])
        self.assertEqual(
            item_result['resref'],
            self.fake_items['op_armor']['resref'])
        self.assertEqual(
            item_result['amount'],
            self.fake_items['op_armor']['amount'])
        # TODO:Created and updated tests

    # Test that we cannot create an item on Meero via create call when admin
    # Because she ain't created
    def test_admin_create_item_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.items_create(
                self.fake_characters['meero'],
                self.fake_items['op_armor'],
                self.accounts['aez'])

    # Test that we cannot create a new armor on Ji'lin via post call when not admin
    # Because Viti's campaign is ridiculous with loot
    def test_not_admin_create_item(self):
        with self.assertRaises(HTTPForbidden):
            self.items_create(
                self.characters['jilin'],
                self.fake_items['cheat_sword'],
                self.accounts['noob'])

    # Test that we can get the Jilin's training via get call when owner
    # Because the noob account owns jilin
    def test_own_get_action(self):
        action_result = self.action_get(
            self.characters['jilin'],
            self.actions['noob_train'],
            self.accounts['noob'])

        self.assert_compare_objects(action_result, self.actions['noob_train'], 
            *Action.__owned__(Action))

    # Test that we cannot get Al's crafting via get call when not owner
    # Because the noob account doesn't own alrunden
    def test_not_own_get_action(self):
        with self.assertRaises(HTTPForbidden):
            self.action_get(
                self.characters['alrunden'],
                self.actions['al_craft'],
                self.accounts['noob'])

    # Test that we can see the Jilin's mining via get call when admin
    # Because admins can access any character
    def test_admin_get_action(self):
        action_result = self.action_get(
            self.characters['jilin'],
            self.actions['noob_mine'],
            self.accounts['aez'])

        self.assert_compare_objects(action_result, self.actions['noob_mine'], 
            *Action.__owned__(Action))

    # Test that we cannot get Al's crafting with Siobhan's id via get call when admin
    # Because those are owned by Al's character, not Siobhan's
    def test_admin_get_action_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.action_get(
                self.characters.get('siobhan'),
                self.actions['al_craft'],
                self.accounts['aez'])

    # Test that we cannot get the noob's cheating via get call when admin
    # Because it ain't created, because the noob can't cheat
    def test_admin_get_action_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.action_get(
                self.characters['jilin'],
                self.fake_actions['noob_cheat'],
                self.accounts['aez'])

    # Test that we can remove Jilin's crafting via delete call when admin
    # Test that crafting is not accessible via get call
    # Because the noob doens't know what he's doing
    def test_admin_delete_action(self):
        actions_result = self.action_delete(
            self.characters['jilin'],
            self.actions['noob_mine'],
            self.accounts['tweek'])

        compare_actions = []
        for key, action in self.actions.items():
            if action['characterId'] == self.characters['jilin']['id']:
                compare_actions.append(action)

        remaining_total = len(compare_actions)-1
        return_total = remaining_total if remaining_total < 10 else 10

        self.assertEqual(actions_result['total'], remaining_total)
        self.assertEqual(
            len(actions_result['actions']), return_total)
        with self.assertRaises(HTTPNotFound):
            self.action_get(
                self.characters['jilin'],
                self.actions['noob_mine'],
                self.accounts['noob'])

    # Test that we cannot delete noob's mining with Siobhan's id via get call when admin
    # Because those are owned by noob's character, not Siobhan's
    def test_admin_delete_action_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.action_delete(
                self.characters.get('siobhan'),
                self.actions['noob_mine'],
                self.accounts['aez'])

    # Test that we cannot delete noob's cheat via delete call when admin
    # Because it ain't created, because the noob can't cheat
    def test_admin_delete_action_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.action_delete(
                self.characters['alrunden'],
                self.fake_actions['noob_cheat'],
                self.accounts['aez'])

    # Test that we cannot remove crafing from Al's actions via delete call when not admin
    # Because they don't own Al's character
    def test_not_owner_delete_action(self):
        with self.assertRaises(HTTPForbidden):
            self.action_delete(
                self.characters['alrunden'],
                self.actions['al_craft'],
                self.accounts['noob'])

    # Test that we can get Jilin's actions via get all call when owner
    def test_own_get_all_action(self):
        total = 10
        offset = 0
        actions_result = self.actions_get_all(
            self.characters['jilin'], self.accounts['noob'])

        owned_actions = []
        for key, action in self.actions.items():
            if action['characterId'] == self.characters['jilin']['id']:
                owned_actions.append(action)

        compare_actions = owned_actions[offset:offset + total]
        self.assertEqual(len(actions_result['actions']), len(compare_actions))
        self.assertEqual(
            actions_result['offset'],
            offset + len(compare_actions))

        total_actions = len(owned_actions)
        self.assertEqual(actions_result['total'], total_actions)

        for action, compare_action in zip(
                actions_result['actions'], compare_actions):
            self.assert_compare_objects(action, compare_action, 
                *Action.__owned__(Action))

    # Test that we can't get Al's actions via get all call when not owner
    # Because you can't see other people's shit
    def test_not_own_get_all_action(self):
        with self.assertRaises(HTTPForbidden):
            self.actions_get_all(
                self.characters['alrunden'],
                self.accounts['noob'])

    # Test that we can get Jilin's actions via get all call when admin
    # Because admins can see everything
    def test_admin_get_all_action(self):
        total = 10
        offset = 0
        actions_result = self.actions_get_all(
            self.characters['jilin'], self.accounts['aez'])

        owned_actions = []
        for key, action in self.actions.items():
            if action['characterId'] == self.characters['jilin']['id']:
                owned_actions.append(action)

        compare_actions = owned_actions[offset:offset + total]
        self.assertEqual(len(actions_result['actions']), len(compare_actions))
        self.assertEqual(
            actions_result['offset'],
            offset + len(compare_actions))

        total_actions = len(owned_actions)
        self.assertEqual(actions_result['total'], total_actions)

        for action, compare_action in zip(
                actions_result['actions'], compare_actions):
            self.assert_compare_objects(action, compare_action, 
                *Action.__owned__(Action))

    # Test that we cannot get Meero's actions via get all call when admin
    # Because she ain't created
    def test_admin_get_all_actions_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.actions_get_all(
                self.fake_characters['meero'],
                self.accounts['aez'])
