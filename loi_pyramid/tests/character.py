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

        self.characters = FixtureHelper.character_data(self)
        for name, character in self.characters.items():
            self.session.add(character)

        self.accounts = FixtureHelper.account_data(self)
        for name, account in self.accounts.items():
            self.session.add(account)

        self.items = FixtureHelper.items_data(self)
        for name, item in self.items.items():
            self.session.add(item)

        self.session.flush()

        self.fake_characters = FixtureHelper.fake_character_data(self)
        self.fake_accounts = FixtureHelper.fake_account_data(self)
        self.fake_items = FixtureHelper.fake_items_data(self)

    #Helper method for get calls to /character/{id}
    def character_get(self, character):
        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}
        request = self.dummy_request(self.session, (self.host+resource))

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for delete calls to /character/{id}
    def character_delete(self, character):
        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}
        request = self.dummy_delete_request(self.session, (self.host+resource))

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.delete().json_body

    #Helper method for update calls to /character/{id}
    def character_update(self, character):
        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}

        character_payload = {
            'accountId' : character.accountId,
            'name'      : character.name,
            'exp'       : character.exp,
            'area'      : character.area,
        }

        request = self.dummy_put_request(
                self.session,
                (self.host+resource),
                character_payload)

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.update().json_body

    #Helper method for get all calls to /characters
    def characters_get_all(self):
        resource = '/characters'
        request = self.dummy_request(self.session, (self.host+resource))

        char_view = CharactersViews(testing.DummyResource(), request)

        return char_view.get().json_body

    #Helper method for get calls for /character/{id}/item/{id}
    def item_get(self, character, item):
        resource = '/character/{}/item/{}'.format(character.id, item.id)
        url_params = {'charId': character.id, 'itemId': item.id}

        request = self.dummy_request(self.session, (self.host+resource))

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for update calls for /character/{id}/item/{id}
    def item_update(self, character, item):
        resource = '/character/{}/item/{}'.format(character.id,item.id)
        url_params = {'charId': character.id, 'itemId': item.id}

        item_payload = {
            'characterId' : item.characterId,
            'blueprintId' : item.blueprintId,
            'amount'      : item.amount
        }

        request = self.dummy_put_request(
                self.session,
                (self.host+resource),
                item_payload)

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.update().json_body

    #Helper method for delete calls for /character/{id}/item/{id}
    def item_delete(self, character, item):
        resource = '/character/{}/item/{}'.format(character.id,item.id)
        url_params = {'charId': character.id, 'itemId': item.id}
        request = self.dummy_delete_request(self.session, (self.host+resource))

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.delete().json_body

    #Helper method for get all calls to /character/{id}/items
    def items_get_all(self, character):
        resource = '/character/{}/items'.format(character.id)
        url_params = {'id': character.id}

        request = self.dummy_request(self.session, (self.host+resource))

        char_view = CharacterItemsViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.get().json_body

    #Helper method for create calls to /character/{id}/items
    def items_create(self, character, item):
        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}

        item_payload = {
            'characterId' : item.characterId,
            'blueprintId' : item.blueprintId,
            'amount'      : item.amount
        }

        request = self.dummy_post_request(
                self.session,
                (self.host+resource),
                item_payload)

        char_view = CharacterItemsViews(testing.DummyResource(), request)
        char_view.url = url_params

        return char_view.create().json_body

    #Test that we can get Ji'Lin via get call when owner
    #Because noob owns Ji'Lin
    def test_owner_get_char(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        character_result = self.character_get(self.characters.get('jilin'))

        self.assertEqual(character_result['accountId'], self.characters.get('jilin').accountId)
        self.assertEqual(character_result['name'], self.characters.get('jilin').name)
        self.assertEqual(character_result['exp'], self.characters.get('jilin').exp)
        self.assertEqual(character_result['area'], self.characters.get('jilin').area)
        self.assertEqual(character_result['created'], self.characters.get('jilin').created)
        self.assertEqual(character_result['updated'], self.characters.get('jilin').updated)

    #Test that we cannot get Siobhan via get call when not owner
    #Because noob doesnt own Siobhan
    def test_not_owner_get_char(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        character_result = self.character_get(self.characters.get('siobhan'))

        self.assertEqual(character_result['accountId'], self.characters.get('siobhan').accountId)
        self.assertEqual(character_result['name'], self.characters.get('siobhan').name)
        self.assertEqual(character_result['created'], self.characters.get('siobhan').created)
        self.assertEqual(character_result['updated'], self.characters.get('siobhan').updated)

        with self.assertRaises(KeyError):
            character_result['exp']
        with self.assertRaises(KeyError):
            character_result['area']

    #Test that we can get Ji'Lin via get call when admin
    #Because admins can look at other peoples' chars
    def test_admin_get_char(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        character_result = self.character_get(self.characters.get('jilin'))

        self.assertEqual(character_result['accountId'], self.characters.get('jilin').accountId)
        self.assertEqual(character_result['name'], self.characters.get('jilin').name)
        self.assertEqual(character_result['exp'], self.characters.get('jilin').exp)
        self.assertEqual(character_result['area'], self.characters.get('jilin').area)
        self.assertEqual(character_result['created'], self.characters.get('jilin').created)
        self.assertEqual(character_result['updated'], self.characters.get('jilin').updated)

    #Test that we cannot get Meero via get call when admin
    #Because she ain't created
    def test_admin_get_char_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.fake_characters.get('meero'))

    #Test that we can update Siobhan's name via put call when admin
    #She got some rp exp
    def test_admin_update_char(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        test_spy = copy.copy(self.characters.get('siobhan'))
        test_spy.exp = 11000

        character_result = self.character_update(test_spy)

        self.assertEqual(character_result['accountId'], test_spy.accountId)
        self.assertEqual(character_result['name'], test_spy.name)
        self.assertEqual(character_result['exp'], test_spy.exp)
        self.assertEqual(character_result['area'], test_spy.area)
        self.assertEqual(character_result['created'], test_spy.created)
        #TODO: Need update test for updated timestamp

    #Test that we cannot update Meero's name via get call when admin
    #Because she ain't created
    def test_admin_update_char_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        test_slave = copy.copy(self.fake_characters.get('meero'))
        test_slave.name = 'A SLAVE'

        with self.assertRaises(HTTPNotFound):
            self.character_update(test_slave)

    #Test that we cannot update Jilin's name via put call when not admin
    #Because only admins can do that
    def test_not_admin_update_char(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        test_drow = copy.copy(self.characters.get('jilin'))
        test_drow.name = 'Jarlaxe'

        with self.assertRaises(HTTPForbidden):
            self.character_update(test_drow)

        #Should we test that the info wasn't altered afterwards?

    #Test that we can delete Arthen via delete call when admin
    #Test that he isn't available via get afterwards
    def test_admin_delete_char(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        characters_result = self.character_delete(self.characters.get('arthen'))

        self.assertEqual(len(characters_result), len(self.characters.keys()) - 1)
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.characters.get('arthen'))

    #Test that we cannot delete Meero when admin
    #Because she ain't created
    def test_admin_delete_char_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        with self.assertRaises(HTTPNotFound):
            self.character_delete(self.fake_characters.get('meero'))

    #Test that we cannot delete Jilin via delete call when not admin
    #Because only admins can do that
    def test_not_admin_delete_char(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        with self.assertRaises(HTTPForbidden):
            self.character_delete(self.characters.get('jilin'))

        #Should we test that the info wasn't altered afterwards?

    #Test that we can get all characters via get all call when admin
    #And that we get the full info payload
    #Because only admins and owners get full payload
    def test_admin_get_all_char(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        characters_result = self.characters_get_all()

        self.assertEqual(len(characters_result), len(self.characters.keys()))
        i = 0
        for char in characters_result:
            compare_char = self.characters.get(list(self.characters.keys())[i])
            self.assertEqual(char['accountId'], compare_char.accountId)
            self.assertEqual(char['name'], compare_char.name)
            self.assertEqual(char['exp'], compare_char.exp)
            self.assertEqual(char['area'], compare_char.area)
            self.assertEqual(char['created'], compare_char.created)
            self.assertEqual(char['updated'], compare_char.updated)

            i += 1

    #Test that we can get all characters via get all call when not admin
    #And that we get the partial info payload
    #Because only admins and owners get full payload
    def test_not_admin_get_all_char(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        characters_result = self.characters_get_all()

        self.assertEqual(len(characters_result), len(self.characters.keys()))
        i = 0
        for char in characters_result:
            compare_char = self.characters.get(list(self.characters.keys())[i])
            self.assertEqual(char['accountId'], compare_char.accountId)
            self.assertEqual(char['name'], compare_char.name)
            self.assertEqual(char['created'], compare_char.created)
            self.assertEqual(char['updated'], compare_char.updated)

            with self.assertRaises(KeyError):
                char['exp']
            with self.assertRaises(KeyError):
                char['area']

            i += 1

    #Test that we can get the Jilin's money via get call when owner
    #Because the noob account owns jilin
    def test_own_get_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        money = self.item_get(self.characters.get('jilin'), self.items.get('noob_money'))

        self.assertEqual(money['characterId'], self.characters.get('jilin').id)
        self.assertEqual(money['blueprintId'], self.items.get('noob_money').blueprintId)
        self.assertEqual(money['amount'], self.items.get('noob_money').amount)
        self.assertEqual(money['created'], self.items.get('noob_money').created)
        self.assertEqual(money['updated'], self.items.get('noob_money').updated)

    #Test that we cannot get the Jilin's money via get call when not owner
    #Because the noob account doesn't own alrunden
    def test_not_own_get_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        with self.assertRaises(HTTPClientError):
            self.item_get(self.characters.get('alrunden'), self.items.get('al_money'))

    #Test that we can get the Jilin's money via get call when admin
    #Because admins can access any character
    def test_admin_get_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        money = self.item_get(self.characters.get('jilin'), self.items.get('noob_money'))

        self.assertEqual(money['characterId'], self.characters.get('jilin').id)
        self.assertEqual(money['blueprintId'], self.items.get('noob_money').blueprintId)
        self.assertEqual(money['amount'], self.items.get('noob_money').amount)
        self.assertEqual(money['created'], self.items.get('noob_money').created)
        self.assertEqual(money['updated'], self.items.get('noob_money').updated)

    #Test that we cannot get Al's cows with Siobhan's id via get call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_get_item_not_assoc(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        with self.assertRaises(HTTPClientError):
            self.item_get(self.characters.get('siobhan'), self.items.get('al_cow'))

    #Test that we cannot get Al's Zombie via get call when admin
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_get_item_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters.get('alrunden'), self.fake_items.get('al_zombie'))

    #Test that we can increase Al's money via put call when admin
    def test_admin_update_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        test_money = copy.copy(self.items.get('al_money'))
        test_money.amount = 200000
        item_result = self.item_update(self.characters.get('alrunden'), test_money)

        self.assertEqual(item_result['characterId'], test_money.characterId)
        self.assertEqual(item_result['blueprintId'], test_money.blueprintId)
        self.assertEqual(item_result['amount'], test_money.amount)
        self.assertEqual(item_result['created'], test_money.created)
        self.assertEqual(item_result['updated'], test_money.updated)

    #Test that we cannot update Al's cows with Siobhan's id via put call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_admin_update_item_not_assoc(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        test_cow = copy.copy(self.items.get('al_cow'))
        test_cow.amount = 9

        with self.assertRaises(HTTPClientError):
            self.item_update(self.characters.get('siobhan'), test_cow)

    #Test that we cannot update Al's Zombie count via put call when admin
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_admin_update_item_not_found(self):
        test_zombie = copy.copy(self.fake_items.get('al_zombie'))
        test_zombie.amount = 5

        with self.assertRaises(HTTPNotFound):
            self.item_update(self.characters.get('alrunden'), test_zombie)

    #Test that we cannot update Jilin's money when not admin
    #Because only admins can do that
    def test_not_admin_update_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        test_money = copy.copy(self.items.get('noob_money'))
        test_money.amount = 45000

        with self.assertRaises(HTTPForbidden):
            self.item_update(self.characters.get('jilin'), test_money)

    #Test that we can remove cows and sheep from Al's items via delete call when admin
    #Test that Cows and Sheeps are not accessible via get call
    #Because Al's farm got stolen from
    def test_admin_delete_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        self.item_delete(self.characters.get('alrunden'), self.items.get('al_cow'))
        items_result = self.item_delete(self.characters.get('alrunden'), self.items.get('al_sheep'))

        compare_items = []
        for key, item in self.items.items():
            if item.characterId == self.characters.get('alrunden').id:
                compare_items.append(item)

        self.assertEqual(len(items_result), len(compare_items) - 2)
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters.get('alrunden'), self.items.get('al_cow'))
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters.get('alrunden'), self.items.get('al_sheep'))

    #Test that we cannot delete Al's cows with Siobhan's id via get call when admin
    #Because those are owned by Al's character, not Siobhan's
    def test_admin_delete_item_not_assoc(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        with self.assertRaises(HTTPClientError):
            self.item_delete(self.characters.get('siobhan'), self.items.get('al_cow'))

    #Test that we cannot get Al's Zombie via delete call when admin
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_delete_item_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        with self.assertRaises(HTTPNotFound):
            self.item_delete(self.characters.get('alrunden'), self.fake_items.get('al_zombie'))

    #Test that we cannot remove cows from Al's items via delete call when not admin
    #Because only admins can do that
    def test_not_admin_delete_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        with self.assertRaises(HTTPForbidden):
            self.item_delete(self.characters.get('alrunden'), self.items.get('al_cow'))

    #Test that we can get Jilin's items via get all call when owner
    def test_own_get_all_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        items_result = self.items_get_all(self.characters.get('jilin'))

        compare_items = []
        for key, item in self.items.items():
            if item.characterId == self.characters.get('jilin').id:
                compare_items.append(item)

        self.assertEqual(len(items_result), len(compare_items))
        i = 0
        for item in items_result:
            compare_item = compare_items[i]
            self.assertEqual(item['characterId'], compare_item.characterId)
            self.assertEqual(item['blueprintId'], compare_item.blueprintId)
            self.assertEqual(item['amount'], compare_item.amount)
            self.assertEqual(item['created'], compare_item.created)
            self.assertEqual(item['updated'], compare_item.updated)

            i += 1

    #Test that we can get Jilin's items via get all call when not owner
    #Because you can't see other people's shit
    def test_not_own_get_all_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        with self.assertRaises(HTTPForbidden):
            self.items_get_all(self.characters.get('alrunden'))

    #Test that we can get Jilin's items via get all call when admin
    #Because admins can see everything
    def test_admin_get_all_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        items_result = self.items_get_all(self.characters.get('jilin'))

        compare_items = []
        for key, item in self.items.items():
            if item.characterId == self.characters.get('jilin').id:
                compare_items.append(item)

        self.assertEqual(len(items_result), len(compare_items))
        i = 0
        for item in items_result:
            compare_item = compare_items[i]
            self.assertEqual(item['characterId'], compare_item.characterId)
            self.assertEqual(item['blueprintId'], compare_item.blueprintId)
            self.assertEqual(item['amount'], compare_item.amount)
            self.assertEqual(item['created'], compare_item.created)
            self.assertEqual(item['updated'], compare_item.updated)

            i += 1

    #Test that we cannot get Meero's items via get all call when admin
    #Because she ain't created
    def test_admin_get_all_items_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.fake_characters.get('meero'))

    #Test that we can create a new armor on Al via post call when admin
    #Because Viti's campaign is ridiculous with loot
    def test_admin_create_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        item_result = self.items_create(self.characters.get('alrunden'), self.fake_items.get('op_armor'))

        self.assertEqual(item_result['characterId'], self.fake_items.get('op_armor').characterId)
        self.assertEqual(item_result['blueprintId'], self.fake_items.get('op_armor').blueprintId)
        self.assertEqual(item_result['amount'], self.fake_items.get('op_armor').amount)
        #TODO:Created and updated tests

    #Test that we cannot create an item on Meero via create call when admin
    #Because she ain't created
    def test_admin_create_item_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('aez').username, permissive=True)
        with self.assertRaises(HTTPNotFound):
            self.items_create(self.fake_characters.get('meero'), self.fake_items.get('op_armor'))

    #Test that we cannot create a new armor on Ji'lin via post call when not admin
    #Because Viti's campaign is ridiculous with loot
    def test_not_admin_create_item(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        with self.assertRaises(HTTPForbidden):
            self.items_create(self.characters.get('jilin'), self.fake_items.get('cheat_sword'))
