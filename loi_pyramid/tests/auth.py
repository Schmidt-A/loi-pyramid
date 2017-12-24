# flake8: noqa
from pyramid.httpexceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden
from pyramid import testing
from ..security import hash_password
import copy

from .base_test import BaseTest
from ..views.auth import AuthViews
from .fixture_helper import FixtureHelper


class TestAuthViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestAuthViews, self).setUp()
        self.init_database()

        from ..models import Account

        self.host = 'http://localhost:6543'

        self.accounts = FixtureHelper.account_data(self)
        for name, account in self.accounts.items():
            self.session.add(account)

        self.session.flush()

        #non existent accounts, to be used for negative testing
        self.fake_accounts = FixtureHelper.fake_account_data(self)

    #helper method for login attempts to /login using username and password
    def login(self, account, password):
        resource = '/login'
        postdata = {
            'user': account.username,
            'pw': password
        }

        request = self.dummy_post_request(self.session, (self.host+resource), postdata)

        av = AuthViews(testing.DummyResource(), request)
        resp = av.login()

        return resp

    #helper method for logout attempts to /logout using session headers
    def logout(self):
        resource = '/logout'

        request = self.dummy_request(self.session, (self.host+resource))

        av = AuthViews(testing.DummyResource(), request)
        resp = av.logout()

        return resp

    #Test that logging in with the correct username and password works
    def test_login_success(self):
        resp = self.login(self.accounts.get('noob'), 'drizzit4ever')

        self.assertEqual(resp.status_code, 200)

    #Test that logging out works with a preexisting login
    def test_logout_success(self):
        self.login(self.accounts.get('tweek'), 'dragon4ever')
        resp = self.logout()

        self.assertEqual(resp.status_code, 200)

    #Testing that logging in with a bad password does not work
    def test_login_bad_password(self):
        with self.assertRaises(HTTPUnauthorized):
            resp = self.login(self.accounts.get('tweek'), 'edor')

    #Test that logging into an uncreated account doesn't work
    #Because Tam hasn't created his account yet
    def test_login_no_account(self):
        with self.assertRaises(HTTPUnauthorized):
            resp = self.login(self.fake_accounts.get('tam'), 'dicks4ever')
