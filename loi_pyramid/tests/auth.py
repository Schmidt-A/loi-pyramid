# flake8: noqa
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.auth import AuthViews
from ..models import Account

log = logging.getLogger(__name__)


class TestAuthViews(BaseTest):

    # Initial setup for these tests
    # Needs to be broken up
    def setUp(self):
        super(TestAuthViews, self).setUp()
        self.init_database()

        accounts_data = self.fixture_helper.account_data()
        self.session.flush()

        self.accounts = self.fixture_helper.convert_to_json(accounts_data)

        # non existent accounts, to be used for negative testing
        self.fake_accounts = self.fixture_helper.fake_account_fixture()

    # helper method for login attempts to /login using username and password
    def login(self, account, password):
        resources = [('login', ('username', ''))]
        postdata = {
            'user': account['username'],
            'pw': password
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        request = self.dummy_request(
            dbsession=self.session,
            headers=headers,
            resources=resources,
            method='POST',
            body=postdata)

        auth_view = AuthViews(testing.DummyResource(), request)
        resp = auth_view.login()

        return resp

    # helper method for logout attempts to /logout using session headers
    def logout(self, account):
        resources = [('logout', ('username', ''))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            account=account)

        auth_view = AuthViews(testing.DummyResource(), request)
        resp = auth_view.logout()

        return resp

    # Test that logging in with the correct username and password works
    # TODO: This should assert headers
    def test_login_success(self):
        resp = self.login(self.accounts['noob'], 'drizzit4ever')
        account_result = resp.json_body

        self.assertEqual(resp.status_code, 200)
        self.assert_compare_objects(account_result, self.accounts['noob'], 
            *Account.__owned__(Account))

    # Test that logging out works with a preexisting login
    # TOOD: This should assert the headers
    def test_logout_success(self):
        resp = self.logout(self.accounts['tweek'])

        self.assertEqual(resp.status_code, 200)

    # Testing that logging in with a bad password does not work
    def test_login_bad_password(self):
        with self.assertRaises(HTTPUnauthorized):
            resp = self.login(self.accounts['tweek'], 'edor')

    # Test that logging into an uncreated account doesn't work
    # Because Tam hasn't created his account yet
    def test_login_no_account(self):
        with self.assertRaises(HTTPUnauthorized):
            resp = self.login(self.fake_accounts['tam'], 'dicks4ever')
