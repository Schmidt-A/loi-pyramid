import unittest
import transaction

from pyramid import testing

def dummy_request(dbsession, url):
    req = testing.DummyRequest(dbsession=dbsession)
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


class TestSingleCharacter(BaseTest):

    def setUp(self):
        super(TestSingleCharacter, self).setUp()
        self.init_database()

        from .models import Character

        self.host = 'http://localhost:6543'

        self.accountId      = 'Tweek'
        self.name           = 'Siobhan Faulkner'
        self.factionName    = 'what'
        self.lastLogin      = 'never'
        self.created        = '23/11/2017'

        character = Character(
                accountId=self.accountId,
                name=self.name,
                factionName=self.factionName,
                lastLogin=self.lastLogin,
                created=self.created
            )
        self.session.add(character)

    def test_get(self):
        from .views.character import CharacterViews

        resource = '/character/1'
        url_params = {'id': 1}

        cv = CharacterViews(testing.DummyResource(),
                dummy_request(self.session, (self.host+resource)))
        cv.url = url_params

        character_get = cv.get()

        self.assertEqual(character_get['accountId'], self.accountId)
