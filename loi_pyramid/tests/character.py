# flake8: noqa
from pyramid.httpexceptions import HTTPNotFound
from pyramid import testing
import copy

from .base_test import BaseTest
from ..views.character import CharacterViews
from ..views.character import CharactersViews
from ..views.character import CharacterInventoryViews
from ..views.character import CharacterItemViews


class TestCharacterViews(BaseTest):

    def setUp(self):
        super(TestCharacterViews, self).setUp()
        self.init_database()

        from ..models import Character, Inventory

        self.host = 'http://localhost:6543'

        #TODO: Fix flask rules for indentation
        fixture = []
        self.siobhan = Character(
                accountId   = 'Tweek',
                name        = 'Siobhan Faulkner',
                lastLogin   = '29/11/2017',
                created     = '23/11/2017')
        fixture.append(self.siobhan)
        self.alrunden = Character(
                accountId   = 'Aez',
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
        self.alGrain = Inventory(
                characterId = 2,
                blueprintId = 'grain',
                amount      = 10,
                created     = None,
                updated     = None)
        fixture.append(self.alGrain)
        self.alCow = Inventory(
                characterId = 2,
                blueprintId = 'cow',
                amount      = 5,
                created     = None,
                updated     = None)
        fixture.append(self.alCow)
        self.alSheep = Inventory(
                characterId = 2,
                blueprintId = 'sheep',
                amount      = 20,
                created     = None,
                updated     = None)
        fixture.append(self.alSheep)
        self.alMoney = Inventory(
                characterId = 2,
                blueprintId = 'gp',
                amount      = 400,
                created     = None,
                updated     = None)
        fixture.append(self.alMoney)
        self.sioMoney = Inventory(
                characterId = 1,
                blueprintId = 'gp',
                amount      = 50,
                created     = None,
                updated     = None)
        fixture.append(self.sioMoney)
        self.session.add_all(fixture)
        self.session.flush()

        #not yet added
        self.op_armor = Inventory(
                characterId = 2,
                blueprintId = 'op_armor',
                amount      = 1,
                created     = None,
                updated     = None)

    def character_get(self, character):

        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}
        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        character_result = cv.get().__json__(request)
        return character_result

    def character_delete(self, character):

        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}
        request = self.dummy_delete_request(self.session, (self.host+resource))

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        cv.delete()

    def characters_get(self):

        resource = '/characters'
        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharactersViews(testing.DummyResource(), request)

        characters_get = []
        for character in cv.get():
            characters_get.append(character.__json__(request))

        return characters_get

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

    def inventory_get(self, character):

        resource = '/character/{}/inventory'.format(character.id)
        url_params = {'id': character.id}

        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharacterInventoryViews(testing.DummyResource(), request)
        cv.url = url_params

        inventory_get = []
        for item in cv.get():
            inventory_get.append(item.__json__(request))

        return inventory_get

    def item_get(self, character, item):

        resource = '/character/{}/inventory/{}'.format(character.id, item.id)
        url_params = {'charId': character.id, 'itemId': item.id}

        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharacterItemViews(testing.DummyResource(), request)
        cv.url = url_params

        item_result = cv.get().__json__(request)

        return item_result

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

    def item_update(self, character, item):

        resource = '/character/{}/inventory/{}'.format(character.id,item.id)
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

    def item_delete(self, character, item):

        resource = '/character/{}/inventory/{}'.format(character.id,item.id)
        url_params = {'charId': character.id, 'itemId': item.id}
        request = self.dummy_delete_request(self.session, (self.host+resource))

        cv = CharacterItemViews(testing.DummyResource(), request)
        cv.url = url_params

        cv.delete()

    def test_siobhan_get(self):
        character_result = self.character_get(self.siobhan)

        self.assertEqual(character_result['id'], self.siobhan.id)
        self.assertEqual(character_result['accountId'], self.siobhan.accountId)
        self.assertEqual(character_result['name'], self.siobhan.name)
        self.assertEqual(character_result['lastLogin'], self.siobhan.lastLogin)
        self.assertEqual(character_result['created'], self.siobhan.created)

    def test_siobhan_al_arthen_get(self):
        characters_result = self.characters_get()

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

    def test_spy_update(self):
        test_spy = copy.copy(self.siobhan)
        test_spy.name = 'A SPY'
        character_result = self.character_update(test_spy)

        self.assertEqual(character_result['name'], test_spy.name)

    def test_arthen_delete(self):
        self.character_delete(self.arthen)
        with self.assertRaises(HTTPNotFound):
            self.character_get(self.arthen)

    def test_al_farm(self):
        inventory_result = self.inventory_get(self.alrunden)

        self.assertEqual(len(inventory_result), 4)
        grain = inventory_result[0]
        cow = inventory_result[1]
        sheep = inventory_result[2]
        gp = inventory_result[3]

        self.assertEqual(grain['characterId'], self.alrunden.id)
        self.assertEqual(grain['blueprintId'], self.alGrain.blueprintId)
        self.assertEqual(grain['amount'], self.alGrain.amount)

        self.assertEqual(cow['characterId'], self.alrunden.id)
        self.assertEqual(cow['blueprintId'], self.alCow.blueprintId)
        self.assertEqual(cow['amount'], self.alCow.amount)

        self.assertEqual(sheep['characterId'], self.alrunden.id)
        self.assertEqual(sheep['blueprintId'], self.alSheep.blueprintId)
        self.assertEqual(sheep['amount'], self.alSheep.amount)

        self.assertEqual(gp['characterId'], self.alrunden.id)
        self.assertEqual(gp['blueprintId'], self.alMoney.blueprintId)
        self.assertEqual(gp['amount'], self.alMoney.amount)

    def test_sio_money(self):
        money = self.item_get(self.siobhan, self.sioMoney)

        self.assertEqual(money['characterId'], self.siobhan.id)
        self.assertEqual(money['blueprintId'], self.sioMoney.blueprintId)
        self.assertEqual(money['amount'], self.sioMoney.amount)

    def test_sio_poor(self):
        test_money = copy.copy(self.sioMoney)
        test_money.amount = 1
        item_result = self.item_update(self.siobhan, test_money)

        self.assertEqual(item_result['characterId'], test_money.characterId)
        self.assertEqual(item_result['blueprintId'], test_money.blueprintId)
        self.assertEqual(item_result['amount'], test_money.amount)

    def test_al_stolen(self):
        self.item_delete(self.alrunden, self.alCow)
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.alrunden, self.alCow)
        self.item_delete(self.alrunden, self.alSheep)
        with self.assertRaises(HTTPNotFound):
            self.item_get(self.alrunden, self.alSheep)

    def test_al_is_in_a_viti_campaign(self):
        item_result = self.inventory_create(self.alrunden, self.op_armor)

        self.assertEqual(item_result['characterId'], self.op_armor.characterId)
        self.assertEqual(item_result['blueprintId'], self.op_armor.blueprintId)
        self.assertEqual(item_result['amount'], self.op_armor.amount)
