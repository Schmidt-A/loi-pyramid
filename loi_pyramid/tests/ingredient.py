# flake8: noqa
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.ingredient import IngredientViews, IngredientsViews
from ..models import Ingredient

log = logging.getLogger(__name__)


class TestIngredientViews(BaseTest):

    # Initial setup for these tests
    # Needs to be broken up
    def setUp(self):
        super(TestIngredientViews, self).setUp()
        self.init_database()

        from ..models import Ingredient

        self.host = 'http://localhost:6543'

        accounts_data = self.fixture_helper.account_data()
        ingredients_data = self.fixture_helper.ingredient_data()
        self.session.flush()

        self.accounts = self.fixture_helper.convert_to_json(accounts_data)
        self.ingredients = self.fixture_helper.convert_to_json(ingredients_data)

        # non existent ingredients, to be used for negative testing
        self.fake_ingredients = self.fixture_helper.fake_ingredient_fixture()

    # Helper method for get calls to /ingredients/{material}
    def ingredient_get(self, ingredient, account):
        resources = [('ingredients', ('material', ingredient['material']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            account=account)

        ingredient_view = IngredientViews(testing.DummyResource(), request)

        return ingredient_view.get().json_body

    # Helper method for get all calls to /ingredients
    def ingredients_get_all(self, account, limit=None, offset=None):
        resources = [('ingredients', ('material', ''))]

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

        ingredient_view = IngredientsViews(testing.DummyResource(), request)

        return ingredient_view.get().json_body

    # Test that we can get Iron stats via get call
    def test_get(self):
        ingredient_result = self.ingredient_get(
            self.ingredients['iron'], self.accounts['noob'])

        self.assert_compare_objects(ingredient_result, self.ingredients['iron'], 
            *Ingredient.__owned__(Ingredient))

    # Test that we cannot get Uranium via get call
    # Because it doesn't exist in Faerun
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.ingredient_get(
                self.fake_ingredients['uranium'],
                self.accounts['tweek'])

    # Test that we can get all ingredients via get all call
    def test_get_all(self):
        limit = 10
        offset = 0
        ingredients_result = self.ingredients_get_all(self.accounts['noob'])

        self.assert_compare_paginated_lists(
            ingredients_result, list(self.ingredients.values()),
            Ingredient, limit, offset, *Ingredient.__public__(Ingredient))
