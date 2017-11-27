from pyramid.httpexceptions import HTTPNotFound

from pyramid.view import view_config, view_defaults

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from . import BaseView

from ..models import Character
from ..decorators import set_authorized
from ..schemas import CharacterUpdateSchema, Invalid


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

    @view_config(request_method='POST')
    def update(self):
        try:
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()
        except NoResultFound:
            raise HTTPNotFound

        schema = CharacterUpdateSchema()

        try:
            post_data = schema.deserialize(self.request.POST)
        except Invalid as e:
            raise HTTPClientError

        #TODO: update this when we know what parts we want people to be able
        # to update
        character.name = post_data['name']
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
