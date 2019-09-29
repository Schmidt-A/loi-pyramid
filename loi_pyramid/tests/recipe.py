# flake8: noqa
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.recipe import RecipeViews, RecipesViews

log = logging.getLogger(__name__)

class TestRecipeViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestRecipeViews, self).setUp()
        self.init_database()

        from ..models import Recipe

        self.host = 'http://localhost:6543'

        self.accounts = self.fixture_helper.account_fixture()
        self.recipes = self.fixture_helper.recipe_fixture()
        self.session.flush()

        #non existent recipes, to be used for negative testing
        self.fake_recipes = self.fixture_helper.fake_recipe_fixture()

    #Helper method for get calls to /recipes/{blueprint}
    def recipe_get(self, recipe, account):
        resources = [('recipes', ('blueprint', recipe['blueprint']))]
        
        request = self.dummy_request(
            dbsession=self.session, 
            resources=resources,
            account=account)

        recipe_view = RecipeViews(testing.DummyResource(), request)

        return recipe_view.get().json_body

    #Helper method for get all calls to /recipes
    def recipes_get_all(self, account, limit=None, offset=None):
        resources = [('recipes', ('blueprint', ''))]

        query = {}
        if limit != None:
            query['limit'] = limit
        if offset != None:
            query['offset'] = offset

        request = self.dummy_request(
            dbsession=self.session, 
            resources=resources,
            query=query,
            account=account)

        recipe_view = RecipesViews(testing.DummyResource(), request)

        return recipe_view.get().json_body

    #Test that we can get the recipe to mine Iron via get call
    def test_get(self):
        recipe_result = self.recipe_get(self.recipes['metal'], self.accounts['tweek'])

        self.assertEqual(recipe_result['name'], self.recipes['metal']['name'])
        self.assertEqual(recipe_result['category'], self.recipes['metal']['category'])
        self.assertEqual(recipe_result['actions'], self.recipes['metal']['actions'])
        self.assertEqual(recipe_result['time'], self.recipes['metal']['time'])
        self.assertEqual(recipe_result['cost'], self.recipes['metal']['cost'])
        self.assertEqual(recipe_result['building'], self.recipes['metal']['building'])

    #Test that we cannot get Lyrium via get call
    #Because it's not a real thing in Faerun
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.recipe_get(self.fake_recipes['lyrium'], self.accounts['tweek'])

    #Test that we can get all recipes via get all call
    def test_get_all(self):
        total = 10
        offset = 0
        recipes_result = self.recipes_get_all(self.accounts['tweek'])

        compare_recipes = list(self.recipes.values())[offset:offset+total]
        self.assertEqual(len(recipes_result['recipes']), len(compare_recipes))
        self.assertEqual(recipes_result['offset'], offset+len(compare_recipes))

        total_recipes = len(list(self.recipes.values()))
        self.assertEqual(recipes_result['total'], total_recipes)

        for recipe, compare_recipe in zip(recipes_result['recipes'], compare_recipes):
            self.assertEqual(recipe['name'], compare_recipe['name'])
            self.assertEqual(recipe['category'], compare_recipe['category'])
            self.assertEqual(recipe['actions'], compare_recipe['actions'])
            self.assertEqual(recipe['cost'], compare_recipe['cost'])
            self.assertEqual(recipe['building'], compare_recipe['building'])

    #Test that we can get all recipes via get all call
    def test_get_all_1st(self):
        total = 1
        offset = 0
        recipes_result = self.recipes_get_all(self.accounts['tweek'], total, offset)

        compare_recipes = list(self.recipes.values())[offset:offset+total]
        self.assertEqual(len(recipes_result['recipes']), len(compare_recipes))
        self.assertEqual(recipes_result['offset'], offset+len(compare_recipes))

        total_recipes = len(list(self.recipes.values()))
        self.assertEqual(recipes_result['total'], total_recipes)

        for recipe, compare_recipe in zip(recipes_result['recipes'], compare_recipes):
            self.assertEqual(recipe['name'], compare_recipe['name'])
            self.assertEqual(recipe['category'], compare_recipe['category'])
            self.assertEqual(recipe['actions'], compare_recipe['actions'])
            self.assertEqual(recipe['cost'], compare_recipe['cost'])
            self.assertEqual(recipe['building'], compare_recipe['building'])
