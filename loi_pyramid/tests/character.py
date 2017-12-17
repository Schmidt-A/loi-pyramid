# flake8: noqa
import copy

from pyramid.httpexceptions import HTTPNotFound
from pyramid import testing

from .base_test import BaseTest
from ..views.character import CharacterViews
from ..views.character import CharactersViews
from ..views.character import CharacterInventoryViews
from ..views.character import CharacterItemViews


class TestCharacterViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestCharacterViews, self).setUp()
        self.init_database()

        from ..models import Character, Inventory

        self.host = 'http://localhost:6543'

        #TODO: Fix flask rules for indentation
        fixture = []
        self.siobhan = Character(
                accountId   = 1,
                name        = 'Siobhan Faulkner',
                lastLogin   = '29/11/2017',
                created     = '23/11/2017')
        fixture.append(self.siobhan)
        self.alrunden = Character(
                accountId   = 2,
                name        = 'Alrunden Peralt',
                lastLogin   = '29/11/2017',
                created     = '26/6/2017')
        fixture.append(self.alrunden)
        self.arthen = Character(
                accountId   = None,
                name        = 'Arthen Relindar',
                lastLogin   = None,
                created     = None)
        fixture.append(self.arthen)
        self.al_grain = Inventory(
                characterId = 2,
                blueprintId = 'grain',
                amount      = 10,
                created     = None,
                updated     = None)
        fixture.append(self.al_grain)
        self.al_cow = Inventory(
                characterId = 2,
                blueprintId = 'cow',
                amount      = 5,
                created     = None,
                updated     = None)
        fixture.append(self.al_cow)
        self.al_sheep = Inventory(
                characterId = 2,
                blueprintId = 'sheep',
                amount      = 20,
                created     = None,
                updated     = None)
        fixture.append(self.al_sheep)
        self.al_money = Inventory(
                characterId = 2,
                blueprintId = 'gp',
                amount      = 400,
                created     = None,
                updated     = None)
        fixture.append(self.al_money)
        self.sio_money = Inventory(
                characterId = 1,
                blueprintId = 'gp',
                amount      = 50,
                created     = None,
                updated     = None)
        fixture.append(self.sio_money)
        self.session.add_all(fixture)
        self.session.flush()

        #non existent character, to be used for negative testing
        self.meero = Character(
                id          = 20,
                accountId   = 2,
                name        = 'Meero Isesi',
                lastLogin   = None,
                created     = None)

        #not yet added, to be used for create
        self.op_armor = Inventory(
                characterId = 2,
                blueprintId = 'op_armor',
                amount      = 1,
                created     = None,
                updated     = None)

        #non existent item, to be used for negative testing
        self.al_zombie = Inventory(
                characterId = 2,
                blueprintId = 'zombie_guard',
                amount      = 2,
                created     = None,
                updated     = None)        

    #Helper method for get calls to /character/{id}
    def character_get(self, character):
        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}
        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        character_result = cv.get().__json__(request)
        return character_result

    #Helper method for delete calls to /character/{id}
    def character_delete(self, character):
        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}
        request = self.dummy_delete_request(self.session, (self.host+resource))

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        cv.delete()

    #Helper method for update calls to /character/{id}
    def character_update(self, character):
        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}

        character_payload = {
            'accountId' : character.accountId,
            'name'      : character.name,
            'lastLogin' : character.lastLogin,
            'created'   : character.created
        }

        request = self.dummy_put_request(
                self.session,
                (self.host+resource),
                character_payload)

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params
        character = cv.update().__json__(request)

        return character

    #Helper method for get all calls to /characters
    def characters_get_all(self):
        resource = '/characters'
        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharactersViews(testing.DummyResource(), request)

        characters_get = []
        for character in cv.get():
            characters_get.append(character.__json__(request))

        return characters_get

    #Helper method for get calls for /character/{id}/item/{id}
    def item_get(self, character, item):
        resource = '/character/{}/item/{}'.format(character.id, item.id)
        url_params = {'charId': character.id, 'itemId': item.id}

        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharacterItemViews(testing.DummyResource(), request)
        cv.url = url_params

        item_result = cv.get().__json__(request)

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

        cv = CharacterItemViews(testing.DummyResource(), request)
        cv.url = url_params
        character = cv.update().__json__(request)

        return character

    #Helper method for delete calls for /character/{id}/item/{id}
    def item_delete(self, character, item):
        resource = '/character/{}/item/{}'.format(character.id,item.id)
        url_params = {'charId': character.id, 'itemId': item.id}
        request = self.dummy_delete_request(self.session, (self.host+resource))

        cv = CharacterItemViews(testing.DummyResource(), request)
        cv.url = url_params
        response = cv.delete()

        inventory_get = []
        for item in response:
            inventory_get.append(item.__json__(request))

        return inventory_get

    #Helper method for get all calls to /character/{id}/inventory
    def inventory_get_all(self, character):
        resource = '/character/{}/inventory'.format(character.id)
        url_params = {'id': character.id}

        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharacterInventoryViews(testing.DummyResource(), request)
        cv.url = url_params
        response = cv.get()

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

        cv = CharacterInventoryViews(testing.DummyResource(), request)
        cv.url = url_params
        item_result = cv.create().__json__(request)

        return item_result

    #Test that we can get Siobhan via get call
    def test_siobhan_get(self):
        character_result = self.character_get(self.siobhan)

        self.assertEqual(character_result['id'], self.siobhan.id)
        self.assertEqual(character_result['accountId'], self.siobhan.accountId)
        self.assertEqual(character_result['name'], self.siobhan.name)
        self.assertEqual(character_result['lastLogin'], self.siobhan.lastLogin)
        self.assertEqual(character_result['created'], self.siobhan.created)

    #Test that we cannot get Meero via get call
    #Because she ain't created
    def test_meero_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.meero)

    #Test that we can update Siobhan's name via put call
    #Because she's a SPYY
    def test_spy_update(self):
        test_spy = copy.copy(self.siobhan)
        test_spy.name = 'A SPY'
        character_result = self.character_update(test_spy)

        self.assertEqual(character_result['name'], test_spy.name)

    #Test that we cannot update Meero's name via get call
    #Because she ain't created
    def test_meero_update_not_found(self):
        test_slave = copy.copy(self.meero)
        test_slave.name = 'A SLAVE'

        with self.assertRaises(HTTPNotFound):
            self.character_update(test_slave)

    #Test that we can delete Arthen via delete call
    #Test that he isn't available via get afterwards
    #Because he's not a real character
    def test_arthen_delete(self):
        self.character_delete(self.arthen)

        with self.assertRaises(HTTPNotFound):
            self.character_get(self.arthen)

    #Test that we cannot delete Meero
    #Because she ain't created
    def test_meero_delete_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.character_delete(self.meero)

    #Test that we can get Siobhan, Alrunden, and Arthen via get all call
    #As those are the only created characters
    def test_siobhan_al_arthen_get(self):
        characters_result = self.characters_get_all()

        self.assertEqual(len(characters_result), 3)
        siobhan = characters_result[0]
        alrunden = characters_result[1]
        arthen = characters_result[2]

        self.assertEqual(siobhan['accountId'], self.siobhan.accountId)
        self.assertEqual(siobhan['name'], self.siobhan.name)
        self.assertEqual(siobhan['lastLogin'], self.siobhan.lastLogin)
        self.assertEqual(siobhan['created'], self.siobhan.created)

        self.assertEqual(alrunden['accountId'], self.alrunden.accountId)
        self.assertEqual(alrunden['name'], self.alrunden.name)
        self.assertEqual(alrunden['lastLogin'], self.alrunden.lastLogin)
        self.assertEqual(alrunden['created'], self.alrunden.created)

        self.assertEqual(arthen['accountId'], self.arthen.accountId)
        self.assertEqual(arthen['name'], self.arthen.name)
        self.assertEqual(arthen['lastLogin'], self.arthen.lastLogin)
        self.assertEqual(arthen['created'], self.arthen.created)

    #Test that we can get Siobhan's money via get call
    def test_sio_money(self):
        money = self.item_get(self.siobhan, self.sio_money)

        self.assertEqual(money['characterId'], self.siobhan.id)
        self.assertEqual(money['blueprintId'], self.sio_money.blueprintId)
        self.assertEqual(money['amount'], self.sio_money.amount)

    #Test that we cannot get Al's Zombie via get call
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_al_zombie_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.alrunden, self.al_zombie)

    #Test that we can decrease Siobhan's money via put call
    #Because Siobhan's poor and spends her money on necessities
    def test_sio_poor(self):
        test_money = copy.copy(self.sio_money)
        test_money.amount = 1
        item_result = self.item_update(self.siobhan, test_money)

        self.assertEqual(item_result['characterId'], test_money.characterId)
        self.assertEqual(item_result['blueprintId'], test_money.blueprintId)
        self.assertEqual(item_result['amount'], test_money.amount)

    #Test that we cannot update Al's Zombie count via put call
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_al_zombie_update_not_found(self):
        test_zombie = copy.copy(self.al_zombie)
        test_zombie.amount = 5

        with self.assertRaises(HTTPNotFound):
            self.item_update(self.alrunden, test_zombie)

    #Test that we can remove cows and sheep from Al's inventory via delete call
    #Test that Cows and Sheeps are not accessible via get call
    #Because Al's farm got stolen from
    def test_al_stolen(self):
        self.item_delete(self.alrunden, self.al_cow)
        inventory_result = self.item_delete(self.alrunden, self.al_sheep)

        self.assertEqual(len(inventory_result), 2)
        grain = inventory_result[0]
        gp = inventory_result[1]

        self.assertEqual(grain['characterId'], self.alrunden.id)
        self.assertEqual(grain['blueprintId'], self.al_grain.blueprintId)
        self.assertEqual(grain['amount'], self.al_grain.amount)

        self.assertEqual(gp['characterId'], self.alrunden.id)
        self.assertEqual(gp['blueprintId'], self.al_money.blueprintId)
        self.assertEqual(gp['amount'], self.al_money.amount)

        with self.assertRaises(HTTPNotFound):
            self.item_get(self.alrunden, self.al_cow)
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.alrunden, self.al_sheep)

    #Test that we cannot get Al's Zombie via delete call
    #Because it ain't created, because Sigmund won't let him have zombies
    def test_al_zombie_delete_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.item_delete(self.alrunden, self.al_zombie)

    #Test that we can get Al's Grain, Cows, Sheep, and Money via get all call
    #Because those are all of the items in Al's inventory
    #Because he's a goddamn farmer
    def test_al_farm(self):
        inventory_result = self.inventory_get_all(self.alrunden)

        self.assertEqual(len(inventory_result), 4)
        grain = inventory_result[0]
        cow = inventory_result[1]
        sheep = inventory_result[2]
        gp = inventory_result[3]

        self.assertEqual(grain['characterId'], self.alrunden.id)
        self.assertEqual(grain['blueprintId'], self.al_grain.blueprintId)
        self.assertEqual(grain['amount'], self.al_grain.amount)

        self.assertEqual(cow['characterId'], self.alrunden.id)
        self.assertEqual(cow['blueprintId'], self.al_cow.blueprintId)
        self.assertEqual(cow['amount'], self.al_cow.amount)

        self.assertEqual(sheep['characterId'], self.alrunden.id)
        self.assertEqual(sheep['blueprintId'], self.al_sheep.blueprintId)
        self.assertEqual(sheep['amount'], self.al_sheep.amount)

        self.assertEqual(gp['characterId'], self.alrunden.id)
        self.assertEqual(gp['blueprintId'], self.al_money.blueprintId)
        self.assertEqual(gp['amount'], self.al_money.amount)

    #Test that we can create a new armor on Al via post call
    #Because Viti's campaign is ridiculous with loot
    def test_viti_gives_al_loot(self):
        item_result = self.inventory_create(self.alrunden, self.op_armor)

        self.assertEqual(item_result['characterId'], self.op_armor.characterId)
        self.assertEqual(item_result['blueprintId'], self.op_armor.blueprintId)
        self.assertEqual(item_result['amount'], self.op_armor.amount)
