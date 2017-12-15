# flake8: noqa
from pyramid.httpexceptions import HTTPNotFound
from pyramid import testing
import copy

from .base_test import BaseTest


class TestAuthViews(BaseTest):

    def setUp(self):
        super(TestAuthViews, self).setUp()

    def test_login_success(self):
        from ..views.auth import AuthViews

        postdata = {
            'user': 'editor',
            'pw': 'editor'
        }
        request = testing.DummyRequest(post=postdata)

        av = AuthViews(testing.DummyResource(), request)
        resp = av.login()

        self.assertEqual(resp.status_code, 200)

    def test_login_failure(self):
        from ..views.auth import AuthViews

        postdata = {
            'user': 'editor',
            'pw': 'edor'
        }
        request = testing.DummyRequest(post=postdata)

        av = AuthViews(testing.DummyResource(), request)
        resp = av.login()

        self.assertEqual(resp.status_code, 401)
