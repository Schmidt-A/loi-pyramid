# flake8: noqa
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPClientError
from pyramid import testing
import copy

from .base_test import BaseTest
from ..views.character import CharacterViews, CharactersViews, CharacterItemsViews, CharacterItemViews
from .fixture_helper import FixtureHelper


class TestCharacterViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestCharacterViews, self).setUp()
        self.init_database()

        self.host = 'http://localhost:6543'

        fixture_data = FixtureHelper(self.session)

        self.characters = fixture_data.character_data()
        self.accounts = fixture_data.account_data()
        self.items = fixture_data.items_data()

        self.session.flush()

        self.fake_characters = fixture_data.fake_character_data()
        self.fake_accounts = fixture_data.fake_account_data()
        self.fake_items = fixture_data.fake_items_data()

    #Helper method for get calls to /character/{id}
    def character_get(self, character, account):
        resource = '/character/{}'.format(character.get('id'))
        url_params = {'id': character.get('id')}
        request = self.dummy_request(self.session, (self.host+resource), account)

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for delete calls to /character/{id}
    def character_delete(self, character, account):
        resource = '/character/{}'.format(character.get('id'))
        url_params = {'id': character.get('id')}
        request = self.dummy_delete_request(self.session, (self.host+resource), account)

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.delete().json_body

    #Helper method for update calls to /character/{id}
    def character_update(self, character, account):
        resource = '/character/{}'.format(character.get('id'))
        url_params = {'id': character.get('id')}

        character_payload = {
            'accountId' : character.get('accountId'),
            'name'      : character.get('name'),
            'exp'       : character.get('exp'),
            'area'      : character.get('area'),
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

    #Helper method for get calls for /character/{id}/item/{id}
    def item_get(self, character, item, account):
        resource = '/character/{}/item/{}'.format(character.get('id'), item.get('id'))
        url_params = {'charId': character.get('id'), 'itemId': item.get('id')}

        request = self.dummy_request(self.session, (self.host+resource), account)

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for update calls for /character/{id}/item/{id}
    def item_update(self, character, item, account):
        resource = '/character/{}/item/{}'.format(character.get('id'),item.get('id'))
        url_params = {'charId': character.get('id'), 'itemId': item.get('id')}

        item_payload = {
            'characterId' : item.get('characterId'),
            'blueprintId' : item.get('blueprintId'),
            'amount'      : item.get('amount')
        }

        request = self.dummy_put_request(
                self.session,
                (self.host+resource),
                item_payload,
                account)

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.update().json_body

    #Helper method for delete calls for /character/{id}/item/{id}
    def item_delete(self, character, item, account):
        resource = '/character/{}/item/{}'.format(character.get('id'),item.get('id'))
        url_params = {'charId': character.get('id'), 'itemId': item.get('id')}
        request = self.dummy_delete_request(self.session, (self.host+resource), account)

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.delete().json_body

    #Helper method for get all calls to /character/{id}/items
    def items_get_all(self, character, account):
        resource = '/character/{}/items'.format(character.get('id'))
        url_params = {'id': character.get('id')}

        request = self.dummy_request(self.session, (self.host+resource), account)

        char_view = CharacterItemsViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for create calls to /character/{id}/items
    def items_create(self, character, item, account):
        resource = '/character/{}'.format(character.get('id'))
        url_params = {'id': character.get('id')}

        item_payload = {
            'characterId' : item.get('characterId'),
            'blueprintId' : item.get('blueprintId'),
            'amount'      : item.get('amount')
        }

        request = self.dummy_post_request(
                self.session,
                (self.host+resource),
                item_payload,
                account)

        char_view = CharacterItemsViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.create().json_body

    #Test that we can get Ji'Lin via get call when owner
    #Because noob owns Ji'Lin
    def test_owner_get_char(self):
        character_result = self.character_get(self.characters.get('jilin'), self.accounts.get('noob'))

        self.assertEqual(character_result['accountId'], self.characters.get('jilin').get('accountId'))
        self.assertEqual(character_result['name'], self.characters.get('jilin').get('name'))
        self.assertEqual(character_result['exp'], self.characters.get('jilin').get('exp'))
        self.assertEqual(character_result['area'], self.characters.get('jilin').get('area'))
        self.assertEqual(character_result['created'], self.characters.get('jilin').get('created'))
        self.assertEqual(character_result['updated'], self.characters.get('jilin').get('updated'))

    #Test that we cannot get Siobhan via get call when not owner
    #Because noob doesnt own Siobhan
    def test_not_owner_get_char(self):
        character_result = self.character_get(self.characters.get('siobhan'), self.accounts.get('noob'))

        self.assertEqual(character_result['accountId'], self.characters.get('siobhan').get('accountId'))
        self.assertEqual(character_result['name'], self.characters.get('siobhan').get('name'))
        self.assertEqual(character_result['created'], self.characters.get('siobhan').get('created'))
        self.assertEqual(character_result['updated'], self.characters.get('siobhan').get('updated'))

        with self.assertRaises(KeyError):
            character_result['exp']
        with self.assertRaises(KeyError):
            character_result['area']

    #Test that we can get Ji'Lin via get call when admin
    #Because admins can look at other peoples' chars
    def test_admin_get_char(self):
        character_result = self.character_get(self.characters.get('jilin'), self.accounts.get('tweek'))

        self.assertEqual(character_result['accountId'], self.characters.get('jilin').get('accountId'))
        self.assertEqual(character_result['name'], self.characters.get('jilin').get('name'))
        self.assertEqual(character_result['exp'], self.characters.get('jilin').get('exp'))
        self.assertEqual(character_result['area'], self.characters.get('jilin').get('area'))
        self.assertEqual(character_result['created'], self.characters.get('jilin').get('created'))
        self.assertEqual(character_result['updated'], self.characters.get('jilin').get('updated'))

    #Test that we cannot get Meero via get call when admin
    #Because she ain't created
    def test_admin_get_char_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.fake_characters.get('meero'), self.accounts.get('tweek'))

    #Test that we can update Siobhan's name via put call when admin
    #She got some rp exp
    def test_admin_update_char(self):
        test_spy = copy.copy(self.characters.get('siobhan'))
        test_spy['exp'] = 11000

        character_result = self.character_update(test_spy, self.accounts.get('tweek'))

        self.assertEqual(character_result['accountId'], test_spy.get('accountId'))
        self.assertEqual(character_result['name'], test_spy.get('name'))
        self.assertEqual(character_result['exp'], test_spy.get('exp'))
        self.assertEqual(character_result['area'], test_spy.get('area'))
        self.assertEqual(character_result['created'], test_spy.get('created'))
        #TODO: Need update test for updated timestamp

    #Test that we cannot update Meero's name via get call when admin
    #Because she ain't created
    def test_admin_update_char_not_found(self):
        test_slave = copy.copy(self.fake_characters.get('meero'))
        test_slave['exp'] = 5000

        with self.assertRaises(HTTPNotFound):
            self.character_update(test_slave, self.accounts.get('tweek'))

    #Test that we cannot update Jilin's name via put call when not admin
    #Because only admins can do that
    def test_not_admin_update_char(self):
        test_drow = copy.copy(self.characters.get('jilin'))
        test_drow['exp'] = 99999999

        with self.assertRaises(HTTPForbidden):
            self.character_update(test_drow, self.accounts.get('noob'))

        #Should we test that the info wasn't altered afterwards?

    #Test that we can delete Arthen via delete call when admin
    #Test that he isn't available via get afterwards
    def test_admin_delete_char(self):
        characters_result = self.character_delete(self.characters.get('arthen'), self.accounts.get('tweek'))

        self.assertEqual(len(characters_result), len(self.characters.keys()) - 1)
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.characters.get('arthen'), self.accounts.get('tweek'))

    #Test that we cannot delete Meero when admin
    #Because she ain't created
    def test_admin_delete_char_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.character_delete(self.fake_characters.get('meero'), self.accounts.get('tweek'))

    #Test that we cannot delete Jilin via delete call when not admin
    #Because only admins can do that
    def test_not_admin_delete_char(self):
        with self.assertRaises(HTTPForbidden):
            self.character_delete(self.characters.get('jilin'), self.accounts.get('noob'))

        #Should we test that the info wasn't altered afterwards?

    #Test that we can get all characters via get all call when admin
    #And that we get the full info payload
    #Because only admins and owners get full payload
    def test_admin_get_all_char(self):
        characters_result = self.characters_get_all(self.accounts.get('tweek'))

        self.assertEqual(len(characters_result), len(self.characters.keys()))
        i = 0
        for char in characters_result:
            compare_char = self.characters.get(list(self.characters.keys())[i])
            self.assertEqual(char['accountId'], compare_char.get('accountId'))
            self.assertEqual(char['name'], compare_char.get('name'))
            self.assertEqual(char['exp'], compare_char.get('exp'))
            self.assertEqual(char['area'], compare_char.get('area'))
            self.assertEqual(char['created'], compare_char.get('created'))
            self.assertEqual(char['updated'], compare_char.get('updated'))
            i += 1

    #Test that we can get all characters via get all call when not admin
    #And that we get the partial info payload
    #Because only admins and owners get full payload
    def test_not_admin_get_all_char(self):
        characters_result = self.characters_get_all(self.accounts.get('noob'))

        self.assertEqual(len(characters_result), len(self.characters.keys()))
        i = 0
        for char in characters_result:
            compare_char = self.characters.get(list(self.characters.keys())[i])
            self.assertEqual(char['accountId'], compare_char.get('accountId'))
            self.assertEqual(char['name'], compare_char.get('name'))
            self.assertEqual(char['created'], compare_char.get('created'))
            self.assertEqual(char['updated'], compare_char.get('updated'))

            with self.assertRaises(KeyError):
                char['exp']
            with self.assertRaises(KeyError):
                char['area']
            i += 1

    #Test that we can get the Jilin's money via get call when owner
    #Because the noob account owns jilin
    def test_own_get_item(self):
        money = self.item_get(self.characters.get('jilin'), self.items.get('noob_money'), self.accounts.get('noob'))

        self.assertEqual(money['characterId'], self.characters.get('jilin').get('id'))
        self.assertEqual(money['blueprintId'], self.items.get('noob_money').get('blueprintId'))
        self.assertEqual(money['amount'], self.items.get('noob_money').get('amount'))
        self.assertEqual(money['created'], self.items.get('noob_money').get('created'))
        self.assertEqual(money['updated'], self.items.get('noob_money').get('updated'))

    #Test that we cannot get the Jilin's money via get call when not owner
    #Because the noob account doesn't own alrunden
    def test_not_own_get_item(self):
        with self.assertRaises(HTTPClientError):
            self.item_get(self.characters.get('alrunden'), self.items.get('al_money'), self.accounts.get('noob'))

    #Test that we can get the Jilin's money via get call when admin
    #Because admins can access any character
    def test_admin_get_item(self):
        money = self.item_get(self.characters.get('jilin'), self.items.get('noob_money'), self.accounts.get('aez'))

        self.assertEqual(money['characterId'], self.characters.get('jilin').get('id'))
        self.assertEqual(money['blueprintId'], self.items.get('noob_money').get('blueprintId'))
        self.assertEqual(money['amount'], self.items.get('noob_money').get('amount'))
        self.assertEqual(money['created'], self.items.get('noob_money').get('created'))
        self.assertEqual(money['updated'], self.items.get('noob_money').get('updated'))

    #Test that we cannot get Al's cows with Siobhan's id via get call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_admin_get_item_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.item_get(self.characters.get('siobhan'), self.items.get('al_cow'), self.accounts.get('aez'))

    #Test that we cannot get Al's Zombie via get call when admin
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_get_item_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters.get('alrunden'), self.fake_items.get('al_zombie'), self.accounts.get('aez'))

    #Test that we can increase Al's money via put call when admin
    def test_admin_update_item(self):
        test_money = copy.copy(self.items.get('al_money'))
        test_money['amount'] = 200000
        item_result = self.item_update(self.characters.get('alrunden'), test_money, self.accounts.get('aez'))

        self.assertEqual(item_result['characterId'], test_money.get('characterId'))
        self.assertEqual(item_result['blueprintId'], test_money.get('blueprintId'))
        self.assertEqual(item_result['amount'], test_money.get('amount'))
        self.assertEqual(item_result['created'], test_money.get('created'))
        self.assertEqual(item_result['updated'], test_money.get('updated'))

    #Test that we cannot update Al's cows with Siobhan's id via put call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_admin_update_item_not_assoc(self):
        test_cow = copy.copy(self.items.get('al_cow'))
        test_cow['amount'] = 9

        with self.assertRaises(HTTPClientError):
            self.item_update(self.characters.get('siobhan'), test_cow, self.accounts.get('aez'))

    #Test that we cannot update Al's Zombie count via put call when admin
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_update_item_not_found(self):
        test_zombie = copy.copy(self.fake_items.get('al_zombie'))
        test_zombie['amount'] = 5

        with self.assertRaises(HTTPNotFound):
            self.item_update(self.characters.get('alrunden'), test_zombie, self.accounts.get('aez'))

    #Test that we cannot update Jilin's money when not admin
    #Because only admins can do that
    def test_not_admin_update_item(self):
        test_money = copy.copy(self.items.get('noob_money'))
        test_money['amount'] = 45000

        with self.assertRaises(HTTPForbidden):
            self.item_update(self.characters.get('jilin'), test_money, self.accounts.get('noob'))

    #Test that we can remove cows and sheep from Al's items via delete call when admin
    #Test that Cows and Sheeps are not accessible via get call
    #Because Al's farm got stolen from
    def test_admin_delete_item(self):
        self.item_delete(self.characters.get('alrunden'), self.items.get('al_cow'), self.accounts.get('aez'))
        items_result = self.item_delete(self.characters.get('alrunden'), self.items.get('al_sheep'), self.accounts.get('aez'))

        compare_items = []
        for key, item in self.items.items():
            if item.get('characterId') == self.characters.get('alrunden').get('id'):
                compare_items.append(item)

        self.assertEqual(len(items_result), len(compare_items) - 2)
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters.get('alrunden'), self.items.get('al_cow'), self.accounts.get('aez'))
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters.get('alrunden'), self.items.get('al_sheep'), self.accounts.get('aez'))

    #Test that we cannot delete Al's cows with Siobhan's id via get call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_admin_delete_item_not_assoc(self):
        with self.assertRaises(HTTPClientError):
            self.item_delete(self.characters.get('siobhan'), self.items.get('al_cow'), self.accounts.get('aez'))

    #Test that we cannot get Al's Zombie via delete call when admin
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_delete_item_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_delete(self.characters.get('alrunden'), self.fake_items.get('al_zombie'), self.accounts.get('aez'))

    #Test that we cannot remove cows from Al's items via delete call when not admin
    #Because only admins can do that
    def test_not_admin_delete_item(self):
        with self.assertRaises(HTTPForbidden):
            self.item_delete(self.characters.get('alrunden'), self.items.get('al_cow'), self.accounts.get('noob'))

    #Test that we can get Jilin's items via get all call when owner
    def test_own_get_all_item(self):
        items_result = self.items_get_all(self.characters.get('jilin'), self.accounts.get('noob'))

        compare_items = []
        for key, item in self.items.items():
            if item.get('characterId') == self.characters.get('jilin').get('id'):
                compare_items.append(item)
        print(items_result)
        print(compare_items)
        self.assertEqual(len(items_result), len(compare_items))
        i = 0
        for item in items_result:
            compare_item = compare_items[i]
            self.assertEqual(item['characterId'], compare_item.get('characterId'))
            self.assertEqual(item['blueprintId'], compare_item.get('blueprintId'))
            self.assertEqual(item['amount'], compare_item.get('amount'))
            self.assertEqual(item['created'], compare_item.get('created'))
            self.assertEqual(item['updated'], compare_item.get('updated'))
            i += 1

    #Test that we can get Jilin's items via get all call when not owner
    #Because you can't see other people's shit
    def test_not_own_get_all_item(self):
        with self.assertRaises(HTTPForbidden):
            self.items_get_all(self.characters.get('alrunden'), self.accounts.get('noob'))

    #Test that we can get Jilin's items via get all call when admin
    #Because admins can see everything
    def test_admin_get_all_item(self):
        items_result = self.items_get_all(self.characters.get('jilin'), self.accounts.get('aez'))

        compare_items = []
        for key, item in self.items.items():
            if item.get('characterId') == self.characters.get('jilin').get('id'):
                compare_items.append(item)

        self.assertEqual(len(items_result), len(compare_items))
        i = 0
        for item in items_result:
            compare_item = compare_items[i]
            self.assertEqual(item['characterId'], compare_item.get('characterId'))
            self.assertEqual(item['blueprintId'], compare_item.get('blueprintId'))
            self.assertEqual(item['amount'], compare_item.get('amount'))
            self.assertEqual(item['created'], compare_item.get('created'))
            self.assertEqual(item['updated'], compare_item.get('updated'))
            i += 1

    #Test that we cannot get Meero's items via get all call when admin
    #Because she ain't created
    def test_admin_get_all_items_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.fake_characters.get('meero'), self.accounts.get('aez'))

    #Test that we can create a new armor on Al via post call when admin
    #Because Viti's campaign is ridiculous with loot
    def test_admin_create_item(self):
        item_result = self.items_create(self.characters.get('alrunden'), self.fake_items.get('op_armor'), self.accounts.get('aez'))

        self.assertEqual(item_result['characterId'], self.fake_items.get('op_armor').get('characterId'))
        self.assertEqual(item_result['blueprintId'], self.fake_items.get('op_armor').get('blueprintId'))
        self.assertEqual(item_result['amount'], self.fake_items.get('op_armor').get('amount'))
        #TODO:Created and updated tests

    #Test that we cannot create an item on Meero via create call when admin
    #Because she ain't created
    def test_admin_create_item_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.items_create(self.fake_characters.get('meero'), self.fake_items.get('op_armor'), self.accounts.get('aez'))

    #Test that we cannot create a new armor on Ji'lin via post call when not admin
    #Because Viti's campaign is ridiculous with loot
    def test_not_admin_create_item(self):
        with self.assertRaises(HTTPForbidden):
            self.items_create(self.characters.get('jilin'), self.fake_items.get('cheat_sword'), self.accounts.get('noob'))
