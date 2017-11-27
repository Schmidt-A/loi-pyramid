import unittest
import transaction

from pyramid import testing


def dummy_request(dbsession, url):
    req = testing.DummyRequest(dbsession=dbsession)
    req.path_url = url
    return req

def dummy_post_request(dbsession, url, post):
    req = testing.DummyRequest(dbsession=dbsession, post=post)
    req.path_url = url
    return req


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestCharacterViews(BaseTest):

    def setUp(self):
        super(TestCharacterViews, self).setUp()
        self.init_database()

        from .models import Character

        self.host = 'http://localhost:6543'

        self.accountId      = 'Tweek'
        self.name           = 'Siobhan Faulkner'
        self.factionName    = 'what'
        self.lastLogin      = 'never'
        self.created        = '23/11/2017'

        self.accountIdAl    = 'Aez'
        self.nameAl         = 'Alrunden Peralt'
        self.factionNameAl  = 'Kelemvorites'
        self.lastLoginAl    = 'never'
        self.createdAl      = '26/11/2017'

        siobhan = Character(
                accountId=self.accountId,
                name=self.name,
                factionName=self.factionName,
                lastLogin=self.lastLogin,
                created=self.created
            )
        alrunden = Character(
                accountId=self.accountIdAl,
                name=self.nameAl,
                factionName=self.factionNameAl,
                lastLogin=self.lastLoginAl,
                created=self.createdAl
            )
        self.session.add(siobhan)
        self.session.add(alrunden)

    def test_character_get(self):
        from .views.character import CharacterViews

        resource = '/character/1'
        url_params = {'id': 1}
        request = dummy_request(self.session, (self.host+resource))

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        character_get = cv.get().__json__(request)

        self.assertEqual(character_get['accountId'], self.accountId)
        self.assertEqual(character_get['name'], self.name)
        self.assertEqual(character_get['factionName'], self.factionName)
        self.assertEqual(character_get['lastLogin'], self.lastLogin)
        self.assertEqual(character_get['created'], self.created)

    def test_character_update(self):
        from .views.character import CharacterViews

        resource = '/character/1'
        url_params = {'id': 1}
        test_name = 'Seth Notteel'
        request = dummy_post_request(self.session, (self.host+resource),
                {'name': test_name})

        cv = CharacterViews(testing.DummyResource(), request)
        cv.url = url_params

        character = cv.update().__json__(request)

        self.assertEqual(character['name'], test_name)

    def test_characters_get(self):
        from .views.character import CharactersViews

        resource = '/characters'
        request = dummy_request(self.session, (self.host+resource))

        cv = CharactersViews(testing.DummyResource(), request)

        characters_get = cv.get()

        self.assertGreater(len(characters_get), 1)
        siobhan = characters_get[0].__json__(request)
        alrunden = characters_get[1].__json__(request)

        self.assertEqual(siobhan['accountId'], self.accountId)
        self.assertEqual(siobhan['name'], self.name)
        self.assertEqual(siobhan['factionName'], self.factionName)
        self.assertEqual(siobhan['lastLogin'], self.lastLogin)
        self.assertEqual(siobhan['created'], self.created)

        self.assertEqual(alrunden['accountId'], self.accountIdAl)
        self.assertEqual(alrunden['name'], self.nameAl)
        self.assertEqual(alrunden['factionName'], self.factionNameAl)
        self.assertEqual(alrunden['lastLogin'], self.lastLoginAl)
        self.assertEqual(alrunden['created'], self.createdAl)
