# flake8: noqa
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPClientError
from pyramid import testing
import copy

from .base_test import BaseTest
from ..views.character import CharacterViews, CharactersViews, CharacterItemsViews, CharacterItemViews
from ..views.character import CharacterActionViews, CharacterActionsViews


class TestCharacterViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestCharacterViews, self).setUp()
        self.init_database()

        self.host = 'http://localhost:6543'

        self.accounts = self.fixture_helper.account_data()
        self.characters = self.fixture_helper.character_data()
        self.items = self.fixture_helper.item_data()
        self.actions = self.fixture_helper.action_data()

        self.session.flush()

        self.fake_characters = self.fixture_helper.fake_character_data()
        self.fake_accounts = self.fixture_helper.fake_account_data()
        self.fake_items = self.fixture_helper.fake_item_data()
        self.fake_actions = self.fixture_helper.fake_action_data()

    #Helper method for get calls to /characters/{id}
    def character_get(self, character, account):
        resource = '/characters/{}'.format(character['id'])
        url_params = {'id': character['id']}
        request = self.dummy_request(self.session, (self.host+resource), account)

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for delete calls to /characters/{id}
    def character_delete(self, character, account):
        resource = '/characters/{}'.format(character['id'])
        url_params = {'id': character['id']}
        request = self.dummy_delete_request(self.session, (self.host+resource), account)

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.delete().json_body

    #Helper method for update calls to /characters/{id}
    def character_update(self, character, account):
        resource = '/characters/{}'.format(character['id'])
        url_params = {'id': character['id']}

        character_payload = {
            'accountId' : character['accountId'],
            'name'      : character['name'],
            'exp'       : character['exp'],
            'area'      : character['area'],
        }

        request = self.dummy_put_request(
                self.session,
                (self.host+resource),
                character_payload,
                account)

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.update().json_body

    #Helper method for get all calls to /characters
    def characters_get_all(self, account):
        resource = '/characters'
        request = self.dummy_request(self.session, (self.host+resource), account)

        char_view = CharactersViews(testing.DummyResource(), request)

        return char_view.get().json_body

    #Helper method for get calls for /characters/{id}/item/{id}
    def item_get(self, character, item, account):
        resource = '/characters/{}/item/{}'.format(character['id'], item['id'])
        url_params = {'charId': character['id'], 'itemId': item['id']}

        request = self.dummy_request(self.session, (self.host+resource), account)

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for update calls for /characters/{id}/item/{id}
    def item_update(self, character, item, account):
        resource = '/characters/{}/item/{}'.format(character['id'],item['id'])
        url_params = {'charId': character['id'], 'itemId': item['id']}

        item_payload = {
            'resref' : item['resref'],
            'amount'      : item['amount']
        }

        request = self.dummy_put_request(
                self.session,
                (self.host+resource),
                item_payload,
                account)

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.update().json_body

    #Helper method for delete calls for /characters/{id}/item/{id}
    def item_delete(self, character, item, account):
        resource = '/characters/{}/item/{}'.format(character['id'],item['id'])
        url_params = {'charId': character['id'], 'itemId': item['id']}
        request = self.dummy_delete_request(self.session, (self.host+resource), account)

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.delete().json_body

    #Helper method for get all calls to /characters/{id}/items
    def items_get_all(self, character, account):
        resource = '/characters/{}/items'.format(character['id'])
        url_params = {'id': character['id']}

        request = self.dummy_request(self.session, (self.host+resource), account)

        char_view = CharacterItemsViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for create calls to /characters/{id}/items
    def items_create(self, character, item, account):
        resource = '/characters/{}'.format(character['id'])
        url_params = {'id': character['id']}

        item_payload = {
            'characterId' : item['characterId'],
            'resref' : item['resref'],
            'amount'      : item['amount']
        }

        request = self.dummy_post_request(
                self.session,
                (self.host+resource),
                item_payload,
                account)

        char_view = CharacterItemsViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.create().json_body

    #Helper method for get calls for /characters/{id}/action/{id}
    def action_get(self, character, action, account):
        resource = '/characters/{}/action/{}'.format(character['id'], action['id'])
        url_params = {'charId': character['id'], 'actionId': action['id']}

        request = self.dummy_request(self.session, (self.host+resource), account)

        char_view = CharacterActionViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for get all calls to /characters/{id}/actions
    def actions_get_all(self, character, account):
        resource = '/characters/{}/actions'.format(character['id'])
        url_params = {'id': character['id']}

        request = self.dummy_request(self.session, (self.host+resource), account)

        char_view = CharacterActionsViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for delete calls for /characters/{id}/action/{id}
    def action_delete(self, character, action, account):
        resource = '/characters/{}/action/{}'.format(character['id'],action['id'])
        url_params = {'charId': character['id'], 'actionId': action['id']}
        request = self.dummy_delete_request(self.session, (self.host+resource), account)

        char_view = CharacterActionViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.delete().json_body

    #Helper method for create calls to /characters/{id}/actions
    def actions_create(self, character, action, account):
        resource = '/characters/{}'.format(character['id'])
        url_params = {'id': character['id']}

        action_payload = {
            'amount'      : action['amount'],
            'recipeId' : action['recipeId']
        }

        request = self.dummy_post_request(
                self.session,
                (self.host+resource),
                action_payload,
                account)

        char_view = CharacterActionsViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.create().json_body

    #Test that we can get Ji'Lin via get call when owner
    #Because noob owns Ji'Lin
    def test_owner_get_char(self):
        character_result = self.character_get(self.characters['jilin'], self.accounts['noob'])

        self.assertEqual(character_result['accountId'], self.characters['jilin']['accountId'])
        self.assertEqual(character_result['name'], self.characters['jilin']['name'])
        self.assertEqual(character_result['exp'], self.characters['jilin']['exp'])
        self.assertEqual(character_result['area'], self.characters['jilin']['area'])
        self.assertEqual(character_result['created'], self.characters['jilin']['created'])
        self.assertEqual(character_result['updated'], self.characters['jilin']['updated'])

    #Test that we cannot get Siobhan via get call when not owner
    #Because noob doesnt own Siobhan
    def test_not_owner_get_char(self):
        character_result = self.character_get(self.characters.get('siobhan'), self.accounts['noob'])

        self.assertEqual(character_result['accountId'], self.characters.get('siobhan')['accountId'])
        self.assertEqual(character_result['name'], self.characters.get('siobhan')['name'])
        self.assertEqual(character_result['created'], self.characters.get('siobhan')['created'])
        self.assertEqual(character_result['updated'], self.characters.get('siobhan')['updated'])

        with self.assertRaises(KeyError):
            character_result['exp']
        with self.assertRaises(KeyError):
            character_result['area']

    #Test that we can get Ji'Lin via get call when admin
    #Because admins can look at other peoples' chars
    def test_admin_get_char(self):
        character_result = self.character_get(self.characters['jilin'], self.accounts['tweek'])

        self.assertEqual(character_result['accountId'], self.characters['jilin']['accountId'])
        self.assertEqual(character_result['name'], self.characters['jilin']['name'])
        self.assertEqual(character_result['exp'], self.characters['jilin']['exp'])
        self.assertEqual(character_result['area'], self.characters['jilin']['area'])
        self.assertEqual(character_result['created'], self.characters['jilin']['created'])
        self.assertEqual(character_result['updated'], self.characters['jilin']['updated'])

    #Test that we cannot get Meero via get call when admin
    #Because she ain't created
    def test_admin_get_char_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.fake_characters['meero'], self.accounts['tweek'])

    #Test that we can update Siobhan's name via put call when admin
    #She got some rp exp
    def test_admin_update_char(self):
        test_spy = copy.copy(self.characters.get('siobhan'))
        test_spy['exp'] = 11000

        character_result = self.character_update(test_spy, self.accounts['tweek'])

        self.assertEqual(character_result['accountId'], test_spy['accountId'])
        self.assertEqual(character_result['name'], test_spy['name'])
        self.assertEqual(character_result['exp'], test_spy['exp'])
        self.assertEqual(character_result['area'], test_spy['area'])
        self.assertEqual(character_result['created'], test_spy['created'])
        #TODO: Need update test for updated timestamp

    #Test that we cannot update Meero's name via get call when admin
    #Because she ain't created
    def test_admin_update_char_not_found(self):
        test_slave = copy.copy(self.fake_characters['meero'])
        test_slave['exp'] = 5000

        with self.assertRaises(HTTPNotFound):
            self.character_update(test_slave, self.accounts['tweek'])

    #Test that we cannot update Jilin's name via put call when not admin
    #Because only admins can do that
    def test_not_admin_update_char(self):
        test_drow = copy.copy(self.characters['jilin'])
        test_drow['exp'] = 99999999

        with self.assertRaises(HTTPForbidden):
            self.character_update(test_drow, self.accounts['noob'])

        #Should we test that the info wasn't altered afterwards?

    #Test that we can delete Arthen via delete call when admin
    #Test that he isn't available via get afterwards
    def test_admin_delete_char(self):
        characters_result = self.character_delete(self.characters['arthen'], self.accounts['tweek'])

        self.assertEqual(len(characters_result), len(self.characters.keys()) - 1)
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.characters['arthen'], self.accounts['tweek'])

    #Test that we cannot delete Meero when admin
    #Because she ain't created
    def test_admin_delete_char_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.character_delete(self.fake_characters['meero'], self.accounts['tweek'])

    #Test that we cannot delete Jilin via delete call when not admin
    #Because only admins can do that
    def test_not_admin_delete_char(self):
        with self.assertRaises(HTTPForbidden):
            self.character_delete(self.characters['jilin'], self.accounts['noob'])

        #Should we test that the info wasn't altered afterwards?

    #Test that we can get all characters via get all call when admin
    #And that we get the full info payload
    #Because only admins and owners get full payload
    def test_admin_get_all_char(self):
        characters_result = self.characters_get_all(self.accounts['tweek'])

        compare_chars = list(self.characters.values())

        self.assertEqual(len(characters_result), len(self.characters.keys()))
        i = 0
        for char in characters_result:
            compare_char = compare_chars[i]
            self.assertEqual(char['accountId'], compare_char['accountId'])
            self.assertEqual(char['name'], compare_char['name'])
            self.assertEqual(char['exp'], compare_char['exp'])
            self.assertEqual(char['area'], compare_char['area'])
            self.assertEqual(char['created'], compare_char['created'])
            self.assertEqual(char['updated'], compare_char['updated'])
            i += 1

    #Test that we can get all characters via get all call when not admin
    #And that we get the partial info payload
    #Because only admins and owners get full payload
    def test_not_admin_get_all_char(self):
        characters_result = self.characters_get_all(self.accounts['noob'])

        self.assertEqual(len(characters_result), len(self.characters.keys()))
        i = 0
        for char in characters_result:
            compare_char = self.characters.get(list(self.characters.keys())[i])
            self.assertEqual(char['accountId'], compare_char['accountId'])
            self.assertEqual(char['name'], compare_char['name'])
            self.assertEqual(char['created'], compare_char['created'])
            self.assertEqual(char['updated'], compare_char['updated'])

            with self.assertRaises(KeyError):
                char['exp']
            with self.assertRaises(KeyError):
                char['area']
            i += 1

    #Test that we can get the Jilin's money via get call when owner
    #Because the noob account owns jilin
    def test_own_get_item(self):
        money = self.item_get(self.characters['jilin'], self.items['noob_money'], self.accounts['noob'])

        self.assertEqual(money['characterId'], self.characters['jilin']['id'])
        self.assertEqual(money['resref'], self.items['noob_money']['resref'])
        self.assertEqual(money['amount'], self.items['noob_money']['amount'])
        self.assertEqual(money['created'], self.items['noob_money']['created'])
        self.assertEqual(money['updated'], self.items['noob_money']['updated'])

    #Test that we cannot get the Al's money via get call when not owner
    #Because the noob account doesn't own alrunden
    def test_not_own_get_item(self):
        with self.assertRaises(HTTPClientError):
            self.item_get(self.characters['alrunden'], self.items['al_money'], self.accounts['noob'])

    #Test that we can get the Jilin's money via get call when admin
    #Because admins can access any character
    def test_admin_get_item(self):
        money = self.item_get(self.characters['jilin'], self.items['noob_money'], self.accounts['aez'])

        self.assertEqual(money['characterId'], self.characters['jilin']['id'])
        self.assertEqual(money['resref'], self.items['noob_money']['resref'])
        self.assertEqual(money['amount'], self.items['noob_money']['amount'])
        self.assertEqual(money['created'], self.items['noob_money']['created'])
        self.assertEqual(money['updated'], self.items['noob_money']['updated'])

    #Test that we cannot get Al's cows with Siobhan's id via get call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_admin_get_item_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.item_get(self.characters.get('siobhan'), self.items['al_cow'], self.accounts['aez'])

    #Test that we cannot get Al's Zombie via get call when admin
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_get_item_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters['alrunden'], self.fake_items['al_zombie'], self.accounts['aez'])

    #Test that we can increase Al's money via put call when admin
    def test_admin_update_item(self):
        test_money = copy.copy(self.items['al_money'])
        test_money['amount'] = 200000
        item_result = self.item_update(self.characters['alrunden'], test_money, self.accounts['aez'])

        self.assertEqual(item_result['characterId'], test_money['characterId'])
        self.assertEqual(item_result['resref'], test_money['resref'])
        self.assertEqual(item_result['amount'], test_money['amount'])
        self.assertEqual(item_result['created'], test_money['created'])
        self.assertEqual(item_result['updated'], test_money['updated'])

    #Test that we cannot update Al's cows with Siobhan's id via put call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_admin_update_item_not_assoc(self):
        test_cow = copy.copy(self.items['al_cow'])
        test_cow['amount'] = 9

        with self.assertRaises(HTTPClientError):
            self.item_update(self.characters.get('siobhan'), test_cow, self.accounts['aez'])

    #Test that we cannot update Al's Zombie count via put call when admin
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_update_item_not_found(self):
        test_zombie = copy.copy(self.fake_items['al_zombie'])
        test_zombie['amount'] = 5

        with self.assertRaises(HTTPNotFound):
            self.item_update(self.characters['alrunden'], test_zombie, self.accounts['aez'])

    #Test that we cannot update Jilin's money when not admin
    #Because only admins can do that
    def test_not_admin_update_item(self):
        test_money = copy.copy(self.items['noob_money'])
        test_money['amount'] = 45000

        with self.assertRaises(HTTPForbidden):
            self.item_update(self.characters['jilin'], test_money, self.accounts['noob'])

    #Test that we can remove cows and sheep from Al's items via delete call when admin
    #Test that Cows and Sheeps are not accessible via get call
    #Because Al's farm got stolen from
    def test_admin_delete_item(self):
        self.item_delete(self.characters['alrunden'], self.items['al_cow'], self.accounts['aez'])
        items_result = self.item_delete(self.characters['alrunden'], self.items['al_sheep'], self.accounts['aez'])

        compare_items = []
        for key, item in self.items.items():
            if item['characterId'] == self.characters['alrunden']['id']:
                compare_items.append(item)

        self.assertEqual(len(items_result), len(compare_items) - 2)
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters['alrunden'], self.items['al_cow'], self.accounts['aez'])
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters['alrunden'], self.items['al_sheep'], self.accounts['aez'])

    #Test that we cannot delete Al's cows with Siobhan's id via get call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_admin_delete_item_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.item_delete(self.characters.get('siobhan'), self.items['al_cow'], self.accounts['aez'])

    #Test that we cannot get Al's Zombie via delete call when admin
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_delete_item_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_delete(self.characters['alrunden'], self.fake_items['al_zombie'], self.accounts['aez'])

    #Test that we cannot remove cows from Al's items via delete call when not admin
    #Because only admins can do that
    def test_not_admin_delete_item(self):
        with self.assertRaises(HTTPForbidden):
            self.item_delete(self.characters['alrunden'], self.items['al_cow'], self.accounts['noob'])

    #Test that we can get Jilin's items via get all call when owner
    def test_own_get_all_item(self):
        items_result = self.items_get_all(self.characters['jilin'], self.accounts['noob'])

        compare_items = []
        for key, item in self.items.items():
            if item['characterId'] == self.characters['jilin']['id']:
                compare_items.append(item)
        self.assertEqual(len(items_result), len(compare_items))
        i = 0
        for item in items_result:
            compare_item = compare_items[i]
            self.assertEqual(item['characterId'], compare_item['characterId'])
            self.assertEqual(item['resref'], compare_item['resref'])
            self.assertEqual(item['amount'], compare_item['amount'])
            self.assertEqual(item['created'], compare_item['created'])
            self.assertEqual(item['updated'], compare_item['updated'])
            i += 1

    #Test that we can't get Al's items via get all call when not owner
    #Because you can't see other people's shit
    def test_not_own_get_all_item(self):
        with self.assertRaises(HTTPForbidden):
            self.items_get_all(self.characters['alrunden'], self.accounts['noob'])

    #Test that we can get Jilin's items via get all call when admin
    #Because admins can see everything
    def test_admin_get_all_item(self):
        items_result = self.items_get_all(self.characters['jilin'], self.accounts['aez'])

        compare_items = []
        for key, item in self.items.items():
            if item['characterId'] == self.characters['jilin']['id']:
                compare_items.append(item)

        self.assertEqual(len(items_result), len(compare_items))
        i = 0
        for item in items_result:
            compare_item = compare_items[i]
            self.assertEqual(item['characterId'], compare_item['characterId'])
            self.assertEqual(item['resref'], compare_item['resref'])
            self.assertEqual(item['amount'], compare_item['amount'])
            self.assertEqual(item['created'], compare_item['created'])
            self.assertEqual(item['updated'], compare_item['updated'])
            i += 1

    #Test that we cannot get Meero's items via get all call when admin
    #Because she ain't created
    def test_admin_get_all_items_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.items_get_all(self.fake_characters['meero'], self.accounts['aez'])

    #Test that we can create a new armor on Al via post call when admin
    #Because Viti's campaign is ridiculous with loot
    def test_admin_create_item(self):
        item_result = self.items_create(self.characters['alrunden'], self.fake_items['op_armor'], self.accounts['aez'])

        self.assertEqual(item_result['characterId'], self.fake_items['op_armor']['characterId'])
        self.assertEqual(item_result['resref'], self.fake_items['op_armor']['resref'])
        self.assertEqual(item_result['amount'], self.fake_items['op_armor']['amount'])
        #TODO:Created and updated tests

    #Test that we cannot create an item on Meero via create call when admin
    #Because she ain't created
    def test_admin_create_item_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.items_create(self.fake_characters['meero'], self.fake_items['op_armor'], self.accounts['aez'])

    #Test that we cannot create a new armor on Ji'lin via post call when not admin
    #Because Viti's campaign is ridiculous with loot
    def test_not_admin_create_item(self):
        with self.assertRaises(HTTPForbidden):
            self.items_create(self.characters['jilin'], self.fake_items['cheat_sword'], self.accounts['noob'])

    #Test that we can get the Jilin's training via get call when owner
    #Because the noob account owns jilin
    def test_own_get_action(self):
        train = self.action_get(self.characters['jilin'], self.actions['noob_train'], self.accounts['noob'])

        self.assertEqual(train['characterId'], self.characters['jilin']['id'])
        self.assertEqual(train['resref'], self.actions['noob_train']['resref'])
        self.assertEqual(train['amount'], self.actions['noob_train']['amount'])
        self.assertEqual(train['recipeId'], self.actions['noob_train']['recipeId'])
        self.assertEqual(train['ingredients'], self.actions['noob_train']['ingredients'])
        self.assertEqual(train['completed'], self.actions['noob_train']['completed'])

    #Test that we cannot get Al's crafting via get call when not owner
    #Because the noob account doesn't own alrunden
    def test_not_own_get_action(self):
        with self.assertRaises(HTTPClientError):
            self.action_get(self.characters['alrunden'], self.actions['al_craft'], self.accounts['noob'])

    #Test that we can see the Jilin's mining via get call when admin
    #Because admins can access any character
    def test_admin_get_action(self):
        mining = self.action_get(self.characters['jilin'], self.actions['noob_mine'], self.accounts['aez'])

        self.assertEqual(mining['characterId'], self.characters['jilin']['id'])
        self.assertEqual(mining['resref'], self.actions['noob_mine']['resref'])
        self.assertEqual(mining['amount'], self.actions['noob_mine']['amount'])
        self.assertEqual(mining['recipeId'], self.actions['noob_mine']['recipeId'])
        self.assertEqual(mining['ingredients'], self.actions['noob_mine']['ingredients'])
        self.assertEqual(mining['completed'], self.actions['noob_mine']['completed'])

    #Test that we cannot get Al's crafting with Siobhan's id via get call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_admin_get_action_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.action_get(self.characters.get('siobhan'), self.actions['al_craft'], self.accounts['aez'])

    #Test that we cannot get the noob's cheating via get call when admin
    #Because it ain't created, because the noob can't cheat
    def test_admin_get_action_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.action_get(self.characters['jilin'], self.fake_actions['noob_cheat'], self.accounts['aez'])

    #Test that we can remove Al's crafting via delete call when admin
    #Test that crafting is not accessible via get call
    #Because the noob doens't know what he's doing
    def test_owner_delete_action(self):
        actions_result = self.action_delete(self.characters['jilin'], self.actions['noob_mine'], self.accounts['noob'])

        compare_actions = []
        for key, action in self.actions.items():
            if action['characterId'] == self.characters['jilin']['id']:
                compare_actions.append(action)

        self.assertEqual(len(actions_result), len(compare_actions) - 1)
        with self.assertRaises(HTTPNotFound):
            self.action_get(self.characters['jilin'], self.actions['noob_mine'], self.accounts['noob'])

    #Test that we cannot delete noob's mining with Siobhan's id via get call when admin
    #Because those are owned by noob's character, not Siobhan's
    def test_admin_delete_action_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.action_delete(self.characters.get('siobhan'), self.actions['noob_mine'], self.accounts['aez'])

    #Test that we cannot delete noob's cheat via delete call when admin
    #Because it ain't created, because the noob can't cheat
    def test_admin_delete_action_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.action_delete(self.characters['alrunden'], self.fake_actions['noob_cheat'], self.accounts['aez'])

    #Test that we cannot remove crafing from Al's actions via delete call when not admin
    #Because they don't own Al's character
    def test_not_owner_delete_action(self):
        with self.assertRaises(HTTPForbidden):
            self.action_delete(self.characters['alrunden'], self.actions['al_craft'], self.accounts['noob'])

    #Test that we can get Jilin's actions via get all call when owner
    def test_own_get_all_action(self):
        actions_result = self.actions_get_all(self.characters['jilin'], self.accounts['noob'])

        compare_actions = []
        for key, action in self.actions.items():
            if action['characterId'] == self.characters['jilin']['id']:
                compare_actions.append(action)
        self.assertEqual(len(actions_result), len(compare_actions))
        i = 0
        for action in actions_result:
            compare_action = compare_actions[i]
            self.assertEqual(action['characterId'], compare_action['characterId'])
            self.assertEqual(action['resref'], compare_action['resref'])
            self.assertEqual(action['amount'], compare_action['amount'])
            self.assertEqual(action['recipeId'], compare_action['recipeId'])
            self.assertEqual(action['ingredients'], compare_action['ingredients'])
            self.assertEqual(action['completed'], compare_action['completed'])
            i += 1

    #Test that we can't get Al's actions via get all call when not owner
    #Because you can't see other people's shit
    def test_not_own_get_all_action(self):
        with self.assertRaises(HTTPForbidden):
            self.actions_get_all(self.characters['alrunden'], self.accounts['noob'])

    #Test that we can get Jilin's actions via get all call when admin
    #Because admins can see everything
    def test_admin_get_all_action(self):
        actions_result = self.actions_get_all(self.characters['jilin'], self.accounts['aez'])

        compare_actions = []
        for key, action in self.actions.items():
            if action['characterId'] == self.characters['jilin']['id']:
                compare_actions.append(action)

        self.assertEqual(len(actions_result), len(compare_actions))
        i = 0
        for action in actions_result:
            compare_action = compare_actions[i]
            self.assertEqual(action['characterId'], compare_action['characterId'])
            self.assertEqual(action['resref'], compare_action['resref'])
            self.assertEqual(action['amount'], compare_action['amount'])
            self.assertEqual(action['recipeId'], compare_action['recipeId'])
            self.assertEqual(action['ingredients'], compare_action['ingredients'])
            self.assertEqual(action['completed'], compare_action['completed'])
            i += 1

    #Test that we cannot get Meero's actions via get all call when admin
    #Because she ain't created
    def test_admin_get_all_actions_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.actions_get_all(self.fake_characters['meero'], self.accounts['aez'])
