import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError
from pyramid.view import view_config, view_defaults

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Character,Inventory
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

    #This method will almost certainly be locked down since we should not allow any of this to be editable
    #Only admins or nwn (via db) should be able to create new characters or edit new characters
    @view_config(request_method='PUT')
    def update(self):
        try:
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()

            schema = CharacterUpdateSchema()
            put_data = schema.deserialize(self.request.body)
            accountId = put_data.get('accountId')
            name = put_data.get('name')
            lastLogin = put_data.get('lastLogin')
            created = put_data.get('created')

            log.info(
                'update: character/id {}/{} with new data {}'.format(
                    character.name, character.id, put_data['name']))

            if accountId:
                character.accountId = accountId
            if name:
                character.name      = name
            if lastLogin:
                character.lastLogin = lastLogin
            if created:
                character.created   = created

        except NoResultFound:
            log.error(
                'update: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.body))
            raise HTTPClientError

        return character

    #This method will almost certainly be locked down since we should not allow any of this to be editable
    #Only admin server or nwn (via db) should be able to delete characters
    @view_config(request_method='DELETE')
    def delete(self):
        try:
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).delete()

            log.info(
                'delete: character/id {}'.format(self.url['id']))
        except NoResultFound:
            log.error(
                'get: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound


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


@set_authorized
@view_defaults(route_name='character_inventory', renderer='json')
class CharacterInventoryViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            #Maybe remove the char lookup
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()

            inv_query = self.request.dbsession.query(Inventory)
            inventory = inv_query.filter(Inventory.characterId == self.url['id']).all()
            log.info(
                'get: inventory of character/id {}/{}'.format(character.name, character.id))
        except NoResultFound:
            log.error(
                'get: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        return inventory
