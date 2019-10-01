import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Recipe
from ..schemas import RecipeAdminUpdate, Invalid


log = logging.getLogger(__name__)

# Govern calls to a single recipe object /recipes/{blueprint}
@view_defaults(route_name='recipe', renderer='json')
class RecipeViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_one(Recipe)


# Govern calls to all recipe objects /recipes
@view_defaults(route_name='recipes', renderer='json')
class RecipesViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all(Recipe)
