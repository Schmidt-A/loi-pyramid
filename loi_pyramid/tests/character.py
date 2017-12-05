# flake8: noqa
from pyramid import testing

from .base_test import BaseTest


class TestCharacterViews(BaseTest):

    def setUp(self):
        super(TestCharacterViews, self).setUp()
        self.init_database()

        from ..models import Character

        self.host = 'http://localhost:6543'

        #TODO: Fix flask rules for indentation
        self.siobhan = Character(
                accountId   = 'Tweek',
                name        = 'Siobhan Faulkner',
                lastLogin   = '29/11/2017',
                created     = '23/11/2017')
        self.alrunden = Character(
                accountId   = 'Aez',
                name        = 'Alrunden Peralt',
                lastLogin   = '29/11/2017',
                created     = '26/6/2017')
        self.arthen = Character(
                accountId   = None,
                name        = 'Arthen Relindar',
                lastLogin   = None,
                created     = None)
        self.session.add_all([self.siobhan, self.alrunden, self.arthen])
        self.session.flush()

    def character_get(self, character):
        from ..views.character import CharacterViews

        resource = '/character/{}'.format(character.id)
        url_params = {'id': character.id}
        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        character_result = cv.get().__json__(request)
        return character_result

    def test_siobhan_get(self):
        print(self.siobhan.id)
        character_result = self.character_get(self.siobhan)

        self.assertEqual(character_result['id'], self.siobhan.id)
        self.assertEqual(character_result['accountId'], self.siobhan.accountId)
        self.assertEqual(character_result['name'], self.siobhan.name)
        self.assertEqual(character_result['lastLogin'], self.siobhan.lastLogin)
        self.assertEqual(character_result['created'], self.siobhan.created)

    def test_characters_get(self):
        from ..views.character import CharactersViews

        resource = '/characters'
        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharactersViews(testing.DummyResource(), request)

        characters_get = cv.get()

        self.assertGreater(len(characters_get), 2)
        siobhan = characters_get[0].__json__(request)
        alrunden = characters_get[1].__json__(request)
        arthen = characters_get[2].__json__(request)

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

    def test_character_update(self):
        from ..views.character import CharacterViews

        resource = '/character/1'
        url_params = {'id': 1}
        test_name = 'A SPY'
        request = self.dummy_put_request(
                self.session,
                (self.host+resource),
                {'name': test_name})

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params
        character = cv.update().__json__(request)

        self.assertEqual(character['name'], test_name)

    def test_character_delete(self):
        from ..views.character import CharacterViews

        resource = '/character/3'
        url_params = {'id': 3}
        request = self.dummy_delete_request(self.session, (self.host+resource))

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        characters_delete = cv.delete()
