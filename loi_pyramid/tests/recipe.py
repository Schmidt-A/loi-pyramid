# flake8: noqa
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.recipe import RecipeViews, RecipesViews
from ..models import Recipe

log = logging.getLogger(__name__)


class TestRecipeViews(BaseTest):

    # Initial setup for these tests
    # Needs to be broken up
    def setUp(self):
        super(TestRecipeViews, self).setUp()
        self.init_database()

        from ..models import Recipe

        self.host = 'http://localhost:6543'

        accounts_data = self.fixture_helper.account_data()
        recipes_data = self.fixture_helper.recipe_data()
        self.session.flush()

        self.accounts = self.fixture_helper.convert_to_json(accounts_data)
        self.recipes = self.fixture_helper.convert_to_json(recipes_data)

        # non existent recipes, to be used for negative testing
        self.fake_recipes = self.fixture_helper.fake_recipe_fixture()

    # Helper method for get calls to /recipes/{blueprint}
    def recipe_get(self, recipe, account):
        resources = [('recipes', ('blueprint', recipe['blueprint']))]

        request = self.dummy_request(
            dbsession=self.session,
            resources=resources,
            account=account)

        recipe_view = RecipeViews(testing.DummyResource(), request)

        return recipe_view.get().json_body

    # Helper method for get all calls to /recipes
    def recipes_get_all(self, account, limit=None, offset=None):
        resources = [('recipes', ('blueprint', ''))]

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

        recipe_view = RecipesViews(testing.DummyResource(), request)

        return recipe_view.get().json_body

    # Test that we can get the recipe to mine Iron via get call
    def test_get(self):
        recipe_result = self.recipe_get(
            self.recipes['metal'], self.accounts['noob'])

        self.assert_compare_objects(recipe_result, self.recipes['metal'], 
            *Recipe.__owned__(Recipe))

    # Test that we cannot get Lyrium via get call
    # Because it's not a real thing in Faerun
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.recipe_get(
                self.fake_recipes['lyrium'],
                self.accounts['tweek'])

    # Test that we can get all recipes via get all call
    def test_get_all(self):
        limit = 10
        offset = 0
        recipes_result = self.recipes_get_all(self.accounts['noob'])

        self.assert_compare_paginated_lists(
            recipes_result, list(self.recipes.values()),
            Recipe, limit, offset, *Recipe.__public__(Recipe))
