# flake8: noqa
import copy

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.recipe import RecipeViews, RecipesViews


class TestRecipeViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestRecipeViews, self).setUp()
        self.init_database()

        from ..models import Recipe

        self.host = 'http://localhost:6543'

        self.accounts = self.fixture_helper.account_data()
        self.recipes = self.fixture_helper.recipe_data()
        self.session.flush()

        #non existent recipes, to be used for negative testing
        self.fake_recipes = self.fixture_helper.fake_recipe_data()

    #Helper method for get calls to /recipe/{blueprint}
    def recipe_get(self, recipe, user_account):
        resource = '/recipe/{}'.format(recipe['blueprint'])
        url_params = {'blueprint': recipe['blueprint']}
        request = self.dummy_request(self.session, (self.host+resource), user_account)

        recipe_view = RecipeViews(testing.DummyResource(), request)
        recipe_view.url = url_params

        return recipe_view.get().json_body

    #Helper method for get all calls to /recipes
    def recipes_get_all(self, user_account):
        resource = '/recipes'
        request = self.dummy_request(self.session, (self.host+resource), user_account)

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
    #As those are the only two created recipes
    def test_get_all(self):
        recipes_result = self.recipes_get_all(self.accounts['tweek'])

        compare_recipes = list(self.recipes.values())

        self.assertEqual(len(recipes_result), len(compare_recipes))
        i = 0
        for recipe in recipes_result:
            compare_recipe = compare_recipes[i]
            self.assertEqual(recipe['name'], compare_recipe['name'])
            self.assertEqual(recipe['category'], compare_recipe['category'])
            self.assertEqual(recipe['actions'], compare_recipe['actions'])
            self.assertEqual(recipe['time'], compare_recipe['time'])
            self.assertEqual(recipe['cost'], compare_recipe['cost'])
            self.assertEqual(recipe['building'], compare_recipe['building'])
            i += 1
