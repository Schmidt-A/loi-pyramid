import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Area


log = logging.getLogger(__name__)


# Govern calls to all recipe objects /areas
@view_defaults(route_name='areas', renderer='json')
class AreasViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all(Area)
