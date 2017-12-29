# flake8: noqa
import unittest
import transaction

from pyramid import testing

from ..models.meta import Base


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:',
            'loi.auth_enabled': 1
        })
        self.config.include('..models')
        settings = self.config.get_settings()

        from ..models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)

    def dummy_request(self, dbsession, url, account):
        req = testing.DummyRequest(dbsession=dbsession)
        req.path_url = url
        req.account = self.create_testing_session(account)
        return req

    def dummy_post_request(self, dbsession, url, post, account):
        req = testing.DummyRequest(dbsession=dbsession, post=post)
        req.path_url = url
        req.account = self.create_testing_session(account)
        return req

    def dummy_put_request(self, dbsession, url, body, account):
        req = testing.DummyRequest(dbsession=dbsession)
        req.path_url = url
        req.method = 'PUT'
        req.body = body
        req.account = self.create_testing_session(account)
        return req

    def dummy_delete_request(self, dbsession, url, account):
        req = testing.DummyRequest(dbsession=dbsession)
        req.path_url = url
        req.method = 'DELETE'
        req.account = self.create_testing_session(account)
        return req

    def create_testing_session(self, account):
        self.config.testing_securitypolicy(userid=account.get('username'), permissive=True)
        account = DummyAccount(account)
        return account


class DummyAccount():

    def __init__(self, account):
        self.username   = account.get('username')
        self.role       = account.get('role')
        self.approved   = account.get('approved')
        self.banned     = account.get('banned')
