# flake8: noqa
import copy

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.ingredient import IngredientViews, IngredientsViews


class TestIngredientViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestIngredientViews, self).setUp()
        self.init_database()

        from ..models import Ingredient

        self.host = 'http://localhost:6543'

        self.accounts = self.fixture_helper.account_data()
        self.ingredients = self.fixture_helper.ingredient_data()
        self.session.flush()

        #non existent ingredients, to be used for negative testing
        self.fake_ingredients = self.fixture_helper.fake_ingredient_data()

    #Helper method for get calls to /ingredient/{material}
    def ingredient_get(self, ingredient, user_account):
        resource = '/ingredient/{}'.format(ingredient['material'])
        url_params = {'material': ingredient['material']}
        request = self.dummy_request(self.session, (self.host+resource), user_account)

        ingredient_view = IngredientViews(testing.DummyResource(), request)
        ingredient_view.url = url_params

        return ingredient_view.get().json_body

    #Helper method for get all calls to /ingredients
    def ingredients_get_all(self, user_account):
        resource = '/ingredients'
        request = self.dummy_request(self.session, (self.host+resource), user_account)

        ingredient_view = IngredientsViews(testing.DummyResource(), request)

        return ingredient_view.get().json_body

    #Test that we can get Iron stats via get call
    def test_get(self):
        ingredient_result = self.ingredient_get(self.ingredients['iron'], self.accounts['tweek'])

        self.assertEqual(ingredient_result['name'], self.ingredients['iron']['name'])
        self.assertEqual(ingredient_result['category'], self.ingredients['iron']['category'])
        self.assertEqual(ingredient_result['tier'], self.ingredients['iron']['tier'])

    #Test that we cannot get Uranium via get call
    #Because it doesn't exist in Faerun
    def test_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.ingredient_get(self.fake_ingredients['uranium'], self.accounts['tweek'])

    #Test that we can get all ingredients via get all call
    #As those are the only two created ingredients
    def test_get_all(self):
        ingredients_result = self.ingredients_get_all(self.accounts['tweek'])

        compare_ingredients = list(self.ingredients.values())

        self.assertEqual(len(ingredients_result), len(compare_ingredients))
        i = 0
        for ingredient in ingredients_result:
            compare_ingredient = compare_ingredients[i]
            self.assertEqual(ingredient['name'], compare_ingredient['name'])
            self.assertEqual(ingredient['category'], compare_ingredient['category'])
            self.assertEqual(ingredient['tier'], compare_ingredient['tier'])
            i += 1
