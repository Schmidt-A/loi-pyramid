# flake8: noqa
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing
import copy

from .base_test import BaseTest
from ..views.character import CharacterViews, CharactersViews, CharacterInventoryViews, CharacterItemViews
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

        self.inventory = FixtureHelper.inventory_data(self)
        for name, item in self.inventory.items():
            self.session.add(item)

        self.session.flush()

        self.fake_characters = FixtureHelper.fake_character_data(self)
        self.fake_accounts = FixtureHelper.fake_account_data(self)
        self.fake_inventory = FixtureHelper.fake_inventory_data(self)

    #Helper method for get calls to /character/{id}
    def character_get(self, character):
        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}
        request = self.dummy_request(self.session, (self.host+resource))

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        character_result = char_view.get().json_body
        return character_result

    #Helper method for delete calls to /character/{id}
    def character_delete(self, character):
        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}
        request = self.dummy_delete_request(self.session, (self.host+resource))

        char_view = CharacterViews(testing.DummyResource(), request)
        char_view.url = url_params

        response = char_view.delete()

        character_result = []
        for character in response:
            character_result.append(character.__json__(request))

        return character_result

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
        character = char_view.update().__json__(request)

        return character

    #Helper method for get all calls to /characters
    def characters_get_all(self):
        resource = '/characters'
        request = self.dummy_request(self.session, (self.host+resource))

        char_view = CharactersViews(testing.DummyResource(), request)
        character_resp = char_view.get().json_body

        characters_get = []
        for character in character_resp:
            characters_get.append(character)

        return characters_get

    #Helper method for get calls for /character/{id}/item/{id}
    def item_get(self, character, item):
        resource = '/character/{}/item/{}'.format(character.id, item.id)
        url_params = {'charId': character.id, 'itemId': item.id}

        request = self.dummy_request(self.session, (self.host+resource))

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params

        item_result = char_view.get().__json__(request)

        return item_result

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
        character = char_view.update().__json__(request)

        return character

    #Helper method for delete calls for /character/{id}/item/{id}
    def item_delete(self, character, item):
        resource = '/character/{}/item/{}'.format(character.id,item.id)
        url_params = {'charId': character.id, 'itemId': item.id}
        request = self.dummy_delete_request(self.session, (self.host+resource))

        char_view = CharacterItemViews(testing.DummyResource(), request)
        char_view.url = url_params
        response = char_view.delete()

        inventory_get = []
        for item in response:
            inventory_get.append(item.__json__(request))

        return inventory_get

    #Helper method for get all calls to /character/{id}/inventory
    def inventory_get_all(self, character):
        resource = '/character/{}/inventory'.format(character.id)
        url_params = {'id': character.id}

        request = self.dummy_request(self.session, (self.host+resource))

        char_view = CharacterInventoryViews(testing.DummyResource(), request)
        char_view.url = url_params
        response = char_view.get()

        inventory_get = []
        for item in response:
            inventory_get.append(item.__json__(request))

        return inventory_get

    #Helper method for create calls to /character/{id}/inventory
    def inventory_create(self, character, item):
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

        char_view = CharacterInventoryViews(testing.DummyResource(), request)
        char_view.url = url_params
        item_result = char_view.create().__json__(request)

        return item_result

    #Test that we can get Ji'Lin via get call when authorized
    #Because noob owns Ji'Lin
    def test_auth_get(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        character_result = self.character_get(self.characters.get('jilin'))

        self.assertEqual(character_result['accountId'], self.characters.get('jilin').accountId)
        self.assertEqual(character_result['name'], self.characters.get('jilin').name)
        self.assertEqual(character_result['exp'], self.characters.get('jilin').exp)
        self.assertEqual(character_result['area'], self.characters.get('jilin').area)
        self.assertEqual(character_result['created'], self.characters.get('jilin').created)
        self.assertEqual(character_result['updated'], self.characters.get('jilin').updated)

    #Test that we can get Ji'Lin via get call when admin
    #Because Tweek is an admin
    def test_admin_get(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        character_result = self.character_get(self.characters.get('jilin'))

        self.assertEqual(character_result['accountId'], self.characters.get('jilin').accountId)
        self.assertEqual(character_result['name'], self.characters.get('jilin').name)
        self.assertEqual(character_result['exp'], self.characters.get('jilin').exp)
        self.assertEqual(character_result['area'], self.characters.get('jilin').area)
        self.assertEqual(character_result['created'], self.characters.get('jilin').created)
        self.assertEqual(character_result['updated'], self.characters.get('jilin').updated)

    #Test that we cannot get Siobhan via get call when unauthorized
    #Because noob doesnt own Siobhan
    def test_no_auth_get(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        character_result = self.character_get(self.characters.get('siobhan'))

        self.assertEqual(character_result['accountId'], self.characters.get('siobhan').accountId)
        self.assertEqual(character_result['name'], self.characters.get('siobhan').name)

        with self.assertRaises(KeyError):
            character_result['exp']
        with self.assertRaises(KeyError):
            character_result['area']
        with self.assertRaises(KeyError):
            character_result['created']
        with self.assertRaises(KeyError):
            character_result['updated']

    #Test that we cannot get Meero via get call
    #Because she ain't created
    def test_admin_get_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.fake_characters.get('meero'))

    #Test that we can update Siobhan's name via put call
    #Because she's a SPYY
    def test_admin_update(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        test_spy = copy.copy(self.characters.get('siobhan'))
        test_spy.name = 'A SPY'

        character_result = self.character_update(test_spy)

        self.assertEqual(character_result['id'], test_spy.id)
        self.assertEqual(character_result['accountId'], test_spy.accountId)
        self.assertEqual(character_result['name'], test_spy.name)
        self.assertEqual(character_result['exp'], test_spy.exp)
        self.assertEqual(character_result['area'], test_spy.area)
        #self.assertEqual(character_result['created'], test_spy.created)
        #self.assertEqual(character_result['updated'], test_spy.updated)

    #Test that we cannot update Siobhan's name via put call
    #Because noob isn't an admin
    def test_no_admin_update(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        test_spy = copy.copy(self.characters.get('siobhan'))
        test_spy.name = 'A SPY'

        with self.assertRaises(HTTPForbidden):
            self.character_update(test_spy)

        #Should we test that the info wasn't altered afterwards?

    #Test that we cannot update Meero's name via get call
    #Because she ain't created
    def test_admin_update_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        test_slave = copy.copy(self.fake_characters.get('meero'))
        test_slave.name = 'A SLAVE'

        with self.assertRaises(HTTPNotFound):
            self.character_update(test_slave)

    #Test that we can delete Arthen via delete call
    #Test that he isn't available via get afterwards
    #Because he's not a real character
    def test_admin_delete(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        characters_result = self.character_delete(self.characters.get('arthen'))

        self.assertEqual(len(characters_result), len(self.characters.keys()) - 1)

        with self.assertRaises(HTTPNotFound):
            self.character_get(self.characters.get('arthen'))

    #Test that we cannot delete Arthen via delete call
    #Because noob isn't an admin
    def test_not_admin_delete(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        with self.assertRaises(HTTPForbidden):
            self.character_delete(self.characters.get('arthen'))

        #Should we test that the info wasn't altered afterwards?

    #Test that we cannot delete Meero
    #Because she ain't created
    def test_admin_delete_not_found(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('tweek').username, permissive=True)
        with self.assertRaises(HTTPNotFound):
            self.character_delete(self.fake_characters.get('meero'))

    #Test that we can get Siobhan, Alrunden, Arthen, Ji'lin via get all call
    #As those are the only created characters
    #You're acting as if you're an admin account
    def test_admin_get_all(self):
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

    #Test that we can get Siobhan, Alrunden, Arthen, and Ji'lin via get all call
    #As those are the only created characters
    #You're acting as if you're an admin account
    def test_no_admin_get_all(self):
        self.config.testing_securitypolicy(userid=self.accounts.get('noob').username, permissive=True)
        characters_result = self.characters_get_all()

        self.assertEqual(len(characters_result), len(self.characters.keys()))
        i = 0
        for char in characters_result:
            compare_char = self.characters.get(list(self.characters.keys())[i])
            self.assertEqual(char['accountId'], compare_char.accountId)
            self.assertEqual(char['name'], compare_char.name)
            with self.assertRaises(KeyError):
                char['exp']
            with self.assertRaises(KeyError):
                char['area']
            with self.assertRaises(KeyError):
                char['created']
            with self.assertRaises(KeyError):
                char['updated']
            i += 1

    #Test that we can get Siobhan's money via get call
    def test_sio_money(self):
        money = self.item_get(self.characters.get('siobhan'), self.inventory.get('sio_money'))

        self.assertEqual(money['characterId'], self.characters.get('siobhan').id)
        self.assertEqual(money['blueprintId'], self.inventory.get('sio_money').blueprintId)
        self.assertEqual(money['amount'], self.inventory.get('sio_money').amount)

    #Test that we cannot get Al's Zombie via get call
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_al_zombie_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters.get('alrunden'), self.fake_inventory.get('al_zombie'))

    #Test that we cannot get Al's cows with Siobhan's id via get call
    #Because those are owned by Al's character, not Siobhan's
    def test_sio_get_al_cows(self):
        with self.assertRaises(HTTPForbidden):
            self.item_get(self.characters.get('siobhan'), self.inventory.get('al_cow'))

    #Test that we can decrease Siobhan's money via put call
    #Because Siobhan's poor and spends her money on necessities
    def test_sio_poor(self):
        test_money = copy.copy(self.inventory.get('sio_money'))
        test_money.amount = 1
        item_result = self.item_update(self.characters.get('siobhan'), test_money)

        self.assertEqual(item_result['characterId'], test_money.characterId)
        self.assertEqual(item_result['blueprintId'], test_money.blueprintId)
        self.assertEqual(item_result['amount'], test_money.amount)

    #Test that we cannot update Al's cows with Siobhan's id via put call
    #Because those are owned by Al's character, not Siobhan's
    def test_sio_update_al_cows(self):
        test_cow = copy.copy(self.inventory.get('al_cow'))
        test_cow.amount = 9

        with self.assertRaises(HTTPForbidden):
            self.item_update(self.characters.get('siobhan'), test_cow)

    #Test that we cannot update Al's Zombie count via put call
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_al_zombie_update_not_found(self):
        test_zombie = copy.copy(self.fake_inventory.get('al_zombie'))
        test_zombie.amount = 5

        with self.assertRaises(HTTPNotFound):
            self.item_update(self.characters.get('alrunden'), test_zombie)

    #Test that we cannot delete Al's cows with Siobhan's id via get call
    #Because those are owned by Al's character, not Siobhan's
    def test_sio_delete_al_cows(self):
        with self.assertRaises(HTTPForbidden):
            self.item_delete(self.characters.get('siobhan'), self.inventory.get('al_cow'))

    #Test that we can remove cows and sheep from Al's inventory via delete call
    #Test that Cows and Sheeps are not accessible via get call
    #Because Al's farm got stolen from
    def test_al_stolen(self):
        self.item_delete(self.characters.get('alrunden'), self.inventory.get('al_cow'))
        inventory_result = self.item_delete(self.characters.get('alrunden'), self.inventory.get('al_sheep'))

        self.assertEqual(len(inventory_result), 2)
        grain = inventory_result[0]
        gp = inventory_result[1]

        self.assertEqual(grain['characterId'], self.characters.get('alrunden').id)
        self.assertEqual(grain['blueprintId'], self.inventory.get('al_grain').blueprintId)
        self.assertEqual(grain['amount'], self.inventory.get('al_grain').amount)

        self.assertEqual(gp['characterId'], self.characters.get('alrunden').id)
        self.assertEqual(gp['blueprintId'], self.inventory.get('al_money').blueprintId)
        self.assertEqual(gp['amount'], self.inventory.get('al_money').amount)

        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters.get('alrunden'), self.inventory.get('al_cow'))
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.characters.get('alrunden'), self.inventory.get('al_sheep'))

    #Test that we cannot get Al's Zombie via delete call
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_al_zombie_delete_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_delete(self.characters.get('alrunden'), self.fake_inventory.get('al_zombie'))

    #Test that we can get Al's Grain, Cows, Sheep, and Money via get all call
    #Because those are all of the items in Al's inventory
    #Because he's a goddamn farmer
    def test_al_farm(self):
        inventory_result = self.inventory_get_all(self.characters.get('alrunden'))

        self.assertEqual(len(inventory_result), 4)
        grain = inventory_result[0]
        cow = inventory_result[1]
        sheep = inventory_result[2]
        gp = inventory_result[3]

        self.assertEqual(grain['characterId'], self.characters.get('alrunden').id)
        self.assertEqual(grain['blueprintId'], self.inventory.get('al_grain').blueprintId)
        self.assertEqual(grain['amount'], self.inventory.get('al_grain').amount)

        self.assertEqual(cow['characterId'], self.characters.get('alrunden').id)
        self.assertEqual(cow['blueprintId'], self.inventory.get('al_cow').blueprintId)
        self.assertEqual(cow['amount'], self.inventory.get('al_cow').amount)

        self.assertEqual(sheep['characterId'], self.characters.get('alrunden').id)
        self.assertEqual(sheep['blueprintId'], self.inventory.get('al_sheep').blueprintId)
        self.assertEqual(sheep['amount'], self.inventory.get('al_sheep').amount)

        self.assertEqual(gp['characterId'], self.characters.get('alrunden').id)
        self.assertEqual(gp['blueprintId'], self.inventory.get('al_money').blueprintId)
        self.assertEqual(gp['amount'], self.inventory.get('al_money').amount)

    #Test that we can create a new armor on Al via post call
    #Because Viti's campaign is ridiculous with loot
    def test_viti_gives_al_loot(self):
        item_result = self.inventory_create(self.characters.get('alrunden'), self.fake_inventory.get('op_armor'))

        self.assertEqual(item_result['characterId'], self.fake_inventory.get('op_armor').characterId)
        self.assertEqual(item_result['blueprintId'], self.fake_inventory.get('op_armor').blueprintId)
        self.assertEqual(item_result['amount'], self.fake_inventory.get('op_armor').amount)
