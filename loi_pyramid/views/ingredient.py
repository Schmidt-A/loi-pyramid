import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Ingredient
from ..decorators import set_authorized
from ..schemas import IngredientAdminUpdate, Invalid


log = logging.getLogger(__name__)

#Govern calls to a single ingredient object /ingredients/{material}
@set_authorized
@view_defaults(route_name='ingredient', renderer='json')
class IngredientViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Ingredient)
            ingredient = query.filter(Ingredient.material == self.url['material']).one()
            log.info(
                'get: material {}'.format(ingredient.material))

            response = Response(json=ingredient.public_payload, content_type='application/json')

        except NoResultFound:
            log.error(
                'get: ingredient \'{}\' not found'.format(self.url['material']))
            raise HTTPNotFound

        return response


#Govern calls to all ingredient objects /ingredients
@set_authorized
@view_defaults(route_name='ingredients', renderer='json')
class IngredientsViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Ingredient)
            ingredients = query.all()
            log.info('get: all ingredients')

            get_all_data = []
            for ingredient in ingredients:
                get_all_data.append(ingredient.public_payload)

            response = Response(json=get_all_data, content_type='application/json')

        except NoResultFound:
            log.error('get: could not retrieve any ingredients')
            raise HTTPNotFound

        return response
