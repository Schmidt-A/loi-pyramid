import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Ingredient
from ..schemas import IngredientAdminUpdate, Invalid


log = logging.getLogger(__name__)

# Govern calls to a single ingredient object /ingredients/{material}
@view_defaults(route_name='ingredient', renderer='json')
class IngredientViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_one(Ingredient)


# Govern calls to all ingredient objects /ingredients
@view_defaults(route_name='ingredients', renderer='json')
class IngredientsViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all(Ingredient)
