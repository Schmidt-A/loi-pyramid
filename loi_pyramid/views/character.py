import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError
from pyramid.view import view_config, view_defaults

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Character
from ..decorators import set_authorized
from ..schemas import CharacterUpdateSchema, Invalid


log = logging.getLogger(__name__)


@set_authorized
@view_defaults(route_name='character', renderer='json')
class CharacterViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()
            log.info(
                'get: character/id {}/{}'.format(character.name, character.id))
        except NoResultFound:
            log.error(
                'get: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        return character

    @view_config(request_method='POST')
    def update(self):
        try:
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()

            schema = CharacterUpdateSchema()
            post_data = schema.deserialize(self.request.POST)

            # TODO: update this when we know what parts we want people to be able
            # to update
            log.info(
                'update: character/id {}/{} with new data {}'.format(
                    character.name, character.id, post_data['name']))
            character.name = post_data['name']

        except NoResultFound:
            log.error(
                'update: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.POST))
            raise HTTPClientError

        return character


@set_authorized
@view_defaults(route_name='characters', renderer='json')
class CharactersViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Character)
            characters = query.all()
            log.info('get: all characters')
        except NoResultFound:
            log.error('get: could not retrieve any characters')
            raise HTTPNotFound

        return characters
