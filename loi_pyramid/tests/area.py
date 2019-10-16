# flake8: noqa
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.area import AreasViews
from ..models import Area

log = logging.getLogger(__name__)


class TestAreaViews(BaseTest):

    # Initial setup for these tests
    # Needs to be broken up
    def setUp(self):
        super(TestAreaViews, self).setUp()
        self.init_database()

        from ..models import Area

        self.host = 'http://localhost:6543'

        accounts_data = self.fixture_helper.account_data()
        characters_data = self.fixture_helper.character_data()
        areas_data = self.fixture_helper.area_data()
        self.session.flush()

        self.accounts = self.fixture_helper.convert_to_json(accounts_data)
        self.areas = self.fixture_helper.convert_to_json(areas_data)

        # non existent areas, to be used for negative testing
        self.fake_areas = self.fixture_helper.fake_area_fixture()

    # Helper method for get all calls to /areas
    def areas_get_all(self, account, limit=None, offset=None):
        resources = [('areas', ('code', ''))]

        query = {}
        if limit is not None:
            query['limit'] = limit
        if offset is not None:
            query['offset'] = offset

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            query=query,
            account=account)

        area_view = AreasViews(testing.DummyResource(), request)

        return area_view.get().json_body

    # Test that we can get all areas via get all call
    def test_get_all(self):
        limit = 10
        offset = 0
        areas_result = self.areas_get_all(self.accounts['noob'])

        self.assert_compare_paginated_lists(
            areas_result, list(self.areas.values()),
            Area, limit, offset, *Area.__public__(Area))
