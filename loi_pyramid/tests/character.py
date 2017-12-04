# flake8: noqa
import unittest
import transaction

from pyramid import testing

from .base_test import BaseTest

class TestCharacterViews(BaseTest):

    def setUp(self):
        super(TestCharacterViews, self).setUp()
        self.init_database()

        from ..models import Character

        self.host = 'http://localhost:6543'

        self.accountId      = 'Tweek'
        self.name           = 'Siobhan Faulkner'
        self.lastLogin      = 'never'
        self.created        = '23/11/2017'

        self.accountIdAl    = 'Aez'
        self.nameAl         = 'Alrunden Peralt'
        self.lastLoginAl    = 'never'
        self.createdAl      = '26/11/2017'

        siobhan = Character(
                accountId=self.accountId,
                name=self.name,
                lastLogin=self.lastLogin,
                created=self.created
            )
        alrunden = Character(
                accountId=self.accountIdAl,
                name=self.nameAl,
                lastLogin=self.lastLoginAl,
                created=self.createdAl
            )
        self.session.add(siobhan)
        self.session.add(alrunden)

    def test_character_get(self):
        from ..views.character import CharacterViews

        resource = '/character/1'
        url_params = {'id': 1}
        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        character_get = cv.get().__json__(request)

        self.assertEqual(character_get['accountId'], self.accountId)
        self.assertEqual(character_get['name'], self.name)
        self.assertEqual(character_get['lastLogin'], self.lastLogin)
        self.assertEqual(character_get['created'], self.created)

    def test_character_update(self):
        from ..views.character import CharacterViews

        resource = '/character/1'
        url_params = {'id': 1}
        test_name = 'Seth Notteel'
        request = self.dummy_post_request(
                self.session,
                (self.host+resource),
                {'name': test_name})

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        character = cv.update().__json__(request)

        self.assertEqual(character['name'], test_name)

    def test_characters_get(self):
        from ..views.character import CharactersViews

        resource = '/characters'
        request = self.dummy_request(self.session, (self.host+resource))

        cv = CharactersViews(testing.DummyResource(), request)

        characters_get = cv.get()

        self.assertGreater(len(characters_get), 1)
        siobhan = characters_get[0].__json__(request)
        alrunden = characters_get[1].__json__(request)

        self.assertEqual(siobhan['accountId'], self.accountId)
        self.assertEqual(siobhan['name'], self.name)
        self.assertEqual(siobhan['lastLogin'], self.lastLogin)
        self.assertEqual(siobhan['created'], self.created)

        self.assertEqual(alrunden['accountId'], self.accountIdAl)
        self.assertEqual(alrunden['name'], self.nameAl)
        self.assertEqual(alrunden['lastLogin'], self.lastLoginAl)
        self.assertEqual(alrunden['created'], self.createdAl)
