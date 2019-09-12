import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Recipe
from ..schemas import RecipeAdminUpdate, Invalid


log = logging.getLogger(__name__)

#Govern calls to a single recipe object /recipes/{blueprint}
@view_defaults(route_name='recipe', renderer='json')
class RecipeViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Recipe)
            recipe = query.filter(Recipe.blueprint == self.url['blueprint']).one()
            log.info(
                'get: blueprint {}'.format(recipe.blueprint))

            response = Response(json=recipe.public_payload, content_type='application/json')

        except NoResultFound:
            log.error(
                'get: recipe \'{}\' not found'.format(self.url['blueprint']))
            raise HTTPNotFound

        return response


#Govern calls to all recipe objects /recipes
@view_defaults(route_name='recipes', renderer='json')
class RecipesViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Recipe)
            recipes = query.all()
            log.info('get: all recipes')

            get_all_data = []
            for recipe in recipes:
                get_all_data.append(recipe.public_payload)

            response = Response(json=get_all_data, content_type='application/json')

        except NoResultFound:
            log.error('get: could not retrieve any recipes')
            raise HTTPNotFound

        return response
