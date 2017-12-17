import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPCreated
from pyramid.view import view_config, view_defaults

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Character, Inventory
from ..decorators import set_authorized
from ..schemas import CharacterUpdateSchema, InventoryUpdateSchema, Invalid


log = logging.getLogger(__name__)

#Govern calls to a single character object /character/{id}
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
    #I'm not going to expose a new api for making new characters, that should be done by NWN only
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
                character.name = name
            if lastLogin:
                character.lastLogin = lastLogin
            if created:
                character.created = created

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

            #This dumb shit is only needed because we don't throw a not found error if it's not there
            query.filter(Character.id == self.url['id']).one()

            query.filter(Character.id == self.url['id']).delete()
            log.info(
                'delete: character/id {}'.format(self.url['id']))

            #we should return the full list of characters for a delete attempt
            characters = self.request.dbsession.query(Character).all()

        except NoResultFound:
            log.error(
                'get: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        return characters

#Govern calls to all character objects /characters
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

#Govern calls to an item on a character /character/{id}/item/{id}
@set_authorized
@view_defaults(route_name='character_item', renderer='json')
class CharacterItemViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            #Maybe remove the char lookup?
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['charId']).one()

            item_query = self.request.dbsession.query(Inventory)
            item = item_query.filter(Inventory.id == self.url['itemId']).one()

            if character.id == item.characterId:
                log.info(
                    'get: item {}/{} of character/id {}/{}'.format(item.blueprintId, item.id, character.name, character.id))
            else:
                log.error(
                    'update: item id \'{}\' not associated with char id \'{}\''.format(self.url['itemId'],self.url['charId']))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'get: character id \'{}\' not found'.format(self.url['charId']))
            raise HTTPNotFound

        return item

    #This method will almost certainly be locked down since we should not allow any of this to be editable
    #Only admins or nwn (via db) should be able to create new characters or edit new characters
    @view_config(request_method='PUT')
    def update(self):
        try:
            #Maybe remove the char lookup?
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['charId']).one()

            item_query = self.request.dbsession.query(Inventory)
            item = item_query.filter(Inventory.id == self.url['itemId']).one()

            schema = InventoryUpdateSchema()
            put_data = schema.deserialize(self.request.body)
            amount = put_data.get('amount')

            if character.id == item.characterId:
                log.info(
                    'update: item/amount {}/{} from character/id {}/{} with new data {}'.format(item.blueprintId, item.amount,
                        character.name, character.id, put_data['amount']))

                if amount:
                    item.amount = amount
            else:
                log.error(
                    'update: item id \'{}\' not associated with char id \'{}\''.format(self.url['itemId'],self.url['charId']))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'update: item id \'{}\' or char id \'{}\' not found'.format(self.url['itemId'],self.url['charId']))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.body))
            raise HTTPClientError

        return item

    #This method will almost certainly be locked down since we should not allow any of this to be editable
    #Only admin server or nwn (via db) should be able to delete characters
    @view_config(request_method='DELETE')
    def delete(self):
        try:
            #Maybe remove the char lookup?
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['charId']).one()

            item_query = self.request.dbsession.query(Inventory)
            item = item_query.filter(Inventory.id == self.url['itemId']).one()

            if character.id == item.characterId:
                item_query.filter(Inventory.id == self.url['itemId']).delete()
                log.info(
                    'delete: item/amount {}/{} from character/id {}/{}'.format(item.blueprintId, item.amount, character.name, character.id))

                #we should return the full list of characters for a delete attempt
                inv_query = self.request.dbsession.query(Inventory)
                inventory = inv_query.filter(Inventory.characterId == self.url['charId']).all()

            else:
                log.error(
                    'update: item id \'{}\' not associated with char id \'{}\''.format(self.url['itemId'],self.url['charId']))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'get: item id \'{}\' or char id \'{}\' not found'.format(self.url['itemId'],self.url['charId']))
            raise HTTPNotFound

        return inventory

#Govern calls to a character's inventory /character/{id}/inventory
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

    #This method will almost certainly be locked down since we should not allow any of this to be editable
    #Only admin server or nwn (via db) should be able to create items
    @view_config(request_method='POST')
    def create(self):
        try:
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()

            schema = InventoryUpdateSchema()
            post_data = schema.deserialize(self.request.POST)

            characterId = character.id
            blueprintId = post_data.get('blueprintId')
            amount = post_data.get('amount')

            newItem = Inventory(
                characterId = characterId, 
                blueprintId = blueprintId, 
                amount      = amount)
            self.request.dbsession.add(newItem)

            log.info(
            'create: item/amount {}/{} from character/id {}/{}'.format(newItem.blueprintId, newItem.amount,
                character.name, character.id))

        except NoResultFound:
            log.error(
                'update: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.POST))
            raise HTTPClientError

        return newItem