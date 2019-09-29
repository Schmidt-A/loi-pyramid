# flake8: noqa
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.ingredient import IngredientViews, IngredientsViews

log = logging.getLogger(__name__)


class TestIngredientViews(BaseTest):

    # Initial setup for these tests
    # Needs to be broken up
    def setUp(self):
        super(TestIngredientViews, self).setUp()
        self.init_database()

        from ..models import Ingredient

        self.host = 'http://localhost:6543'

        self.accounts = self.fixture_helper.account_fixture()
        self.ingredients = self.fixture_helper.ingredient_fixture()
        self.session.flush()

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
            self.ingredients['iron'], self.accounts['tweek'])

        self.assertEqual(
            ingredient_result['name'],
            self.ingredients['iron']['name'])
        self.assertEqual(
            ingredient_result['category'],
            self.ingredients['iron']['category'])
        self.assertEqual(
            ingredient_result['tier'],
            self.ingredients['iron']['tier'])

    # Test that we cannot get Uranium via get call
    # Because it doesn't exist in Faerun
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.ingredient_get(
                self.fake_ingredients['uranium'],
                self.accounts['tweek'])

    # Test that we can get all ingredients via get all call
    def test_get_all(self):
        total = 10
        offset = 0
        ingredients_result = self.ingredients_get_all(self.accounts['tweek'])

        compare_ingredients = list(self.ingredients.values())[
            offset:offset + total]
        self.assertEqual(
            len(ingredients_result['ingredients']), len(compare_ingredients))
        self.assertEqual(
            ingredients_result['offset'],
            offset + len(compare_ingredients))

        total_ingredients = len(list(self.ingredients.values()))
        self.assertEqual(ingredients_result['total'], total_ingredients)

        for ingredient, compare_ingredient in zip(
                ingredients_result['ingredients'], compare_ingredients):
            self.assertEqual(ingredient['name'], compare_ingredient['name'])
            self.assertEqual(
                ingredient['category'],
                compare_ingredient['category'])
            self.assertEqual(ingredient['tier'], compare_ingredient['tier'])
