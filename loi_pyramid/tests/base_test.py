# flake8: noqa
import unittest
import transaction
import logging

from pyramid import testing

from ..models.meta import Base
from .fixture_helper import FixtureHelper
from webob.multidict import MultiDict, NestedMultiDict

log = logging.getLogger(__name__)


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

        self.fixture_helper = FixtureHelper(self.session)
        self.host = 'http://localhost:6543'

    def init_database(self):
        Base.metadata.create_all(self.engine)

        #TODO: required data pattern for tests

    def tearDown(self):
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)

    def dummy_request(
            self,
            dbsession,
            headers={},
            resources=[],
            query=None,
            method='GET',
            body=None,
            account=None):
        req = testing.DummyRequest(dbsession=dbsession)
        req.headers = headers
        req.host_url = self.host

        path = ''
        matchdict = {}
        for resource in resources:
            path += '/{}'.format(resource[0])
            if resource[1][1]:
                path += '/{}'.format(resource[1][1])
                matchdict[resource[1][0]] = resource[1][1]

        req.matchdict = matchdict
        req.path_url = self.host + path
        req.path = path

        # WebOb treats querystring as a multidict
        # using complex querystrings like that is bad practice imo
        # so I do a dict instead and convert it unordered to a multidict
        # https://docs.pylonsproject.org/projects/webob/en/stable/reference.html#query-post-variables
        query_string = ''
        query_dict = MultiDict()
        if query:
            query_string = '?'

            for key, value in query.items():
                query_dict.add(key, value)
                query_string += '{}={}&'.format(key, value)
            query_string = query_string[:-1]
        req.GET = query_dict

        # WebOb only creates the POST object for form bodys with proper content type
        # https://docs.pylonsproject.org/projects/webob/en/stable/reference.html#query-post-variables
        body_dict = MultiDict()
        if body and 'Content-Type' in headers and headers['Content-Type'] == 'application/x-www-form-urlencoded':
            for key, value in body.items():
                body_dict.add(key, value)
        req.POST = body_dict

        # WebOb creates a params that combines them both
        # https://docs.pylonsproject.org/projects/webob/en/stable/reference.html#query-post-variables
        req.params = NestedMultiDict(query_dict, body_dict)

        req.path_qs = path + query_string
        req.query_string = query_string
        req.url = self.host + path + query_string

        req.method = method
        req.body = body

        if account:
            req.account = self.create_testing_session(account)

        return req

    def create_testing_session(self, account):
        self.config.testing_securitypolicy(
            userid=account['username'], permissive=True)
        account = DummyAccount(account)
        return account

    #this assumes that none of the objects have null properties in the args list
    def assert_compare_objects(self, first, second, *args):
        for arg in args:
            self.assertEqual(first[arg], second[arg])

    #this asserts that the lists are of equal length
    def assert_compare_lists(self, first_list, second_list, *args):
        self.assertEqual(len(first_list), len(second_list))
        for first, second in zip (first_list, second_list):
            arg_list = list(map(lambda arg: arg, args))
            self.assert_compare_objects(first, second, *arg_list)

    #
    def assert_not_in_object(self, obj, *args):
        for arg in args:
            with self.assertRaises(KeyError):
                obj[arg]


# Making this because pyramid's request alteration does not translate to unittesting dummy ruquest
# This means that unittesting just doesn't work for many views that utilize this nifty stuff
# So I have to mock up a class object that can be passed with the request
# TODO: honestly, this stuff should probably move to integration tests
class DummyAccount():

    def __init__(self, account):
        self.username = account['username']
        self.role = account['role']
        self.approved = account['approved']
        self.banned = account['banned']

    def is_owner(self, character):
        return self.username == character.accountId

    def is_admin(self):
        return self.role > 2
