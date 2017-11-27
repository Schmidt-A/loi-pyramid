from pyramid.httpexceptions import HTTPNotFound

from pyramid.view import view_config, view_defaults

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from . import BaseView

from ..models import Character
from ..decorators import set_authorized


@set_authorized
@view_defaults(route_name='character', renderer='json')
class CharacterViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()
        except NoResultFound:
            raise HTTPNotFound

        return character


@set_authorized
@view_defaults(route_name='characters', renderer='json')
class CharactersViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Character)
            characters = query.all()
        except NoResultFound:
            raise HTTPNotFound

        return characters
