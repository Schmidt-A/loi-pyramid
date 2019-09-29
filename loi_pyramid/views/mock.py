import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from . import BaseView
from ..models import Account, Character, Action

log = logging.getLogger(__name__)

#TODO: Simplify this - it just needs to be a clean map to the BaseView methods

@view_defaults(route_name='mock', renderer='json')
class MockViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_one(Account)

@view_defaults(route_name='mocks', renderer='json')
class MocksViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all(Account)
    
@view_defaults(route_name='mock_mocks', renderer='json')
class MocksByMockViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all_by_one(Account, Character)

@view_defaults(route_name='mock_mock', renderer='json')
class MockByMockViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_one_by_one(Character, Action)
