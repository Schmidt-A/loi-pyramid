import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Character, Inventory, Account
from ..decorators import set_authorized
from ..schemas import CharacterOwnerSchema, InventoryUpdateSchema, InventoryCreateSchema, Invalid


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

            accountQuery = self.request.dbsession.query(Account)
            account = accountQuery.filter(Account.username == self.request.authenticated_userid).one()

            #if they own it or they're an admin
            if character.accountId == account.username or account.role == 3:
                get_data = {
                    'accountId' : character.accountId,
                    'name'      : character.name,
                    'exp'       : character.exp,
                    'area'      : character.area,
                    'created'   : character.created,
                    'updated'   : character.updated,
                }
                response = Response(json=get_data, content_type='application/json')

            else:
                get_data = {
                    'accountId' : character.accountId,
                    'name'      : character.name
                }
                response = Response(json=get_data, content_type='application/json')

        except NoResultFound:
            log.error(
                'get: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        return response

    #This method will be locked down since we should not allow any of this to be editable
    #Only admins or nwn (via db) should be able to create new characters or edit new characters
    #I'm not going to expose a new api for making new characters, that should be done by NWN only
    @view_config(request_method='PUT')
    def update(self):
        try:
            accountQuery = self.request.dbsession.query(Account)
            account = accountQuery.filter(Account.username == self.request.authenticated_userid).one()

            #if they're an admin they can do everything
            if account.role == 3:
                query = self.request.dbsession.query(Character)
                character = query.filter(Character.id == self.url['id']).one()

                schema = CharacterOwnerSchema()
                put_data = schema.deserialize(self.request.body)
                accountId   = put_data.get('accountId')
                name        = put_data.get('name')
                exp         = put_data.get('exp')
                area        = put_data.get('area')

                if accountId:
                    character.accountId = accountId
                if name:
                    character.name = name
                if exp:
                    character.exp = exp
                if area:
                    character.area = area
                #add updated timestamp

                log.info(
                    'update: character/id {}/{} with new data {}'.format(
                    character.name, character.id, [put_data['accountId'],
                    put_data['name'], put_data['exp'], put_data['area']]))

            else:
                log.error(
                    'update: account/role {}/{} is not allowed to do this'.format(
                        account.username, account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'update: character id \'{}\' or account \'{}\' not found'.format(
                    self.url['id'], self.request.authenticated_userid))
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
            accountQuery = self.request.dbsession.query(Account)
            account = accountQuery.filter(Account.username == self.request.authenticated_userid).one()

            #if they're an admin they can do everything
            if account.role == 3:
                query = self.request.dbsession.query(Character)

                #This dumb shit is only needed because we don't throw a not found error if it's not there
                query.filter(Character.id == self.url['id']).one()

                query.filter(Character.id == self.url['id']).delete()
                log.info(
                    'delete: character/id {}'.format(self.url['id']))

                #we should return the full list of characters for a delete attempt
                characters = self.request.dbsession.query(Character).all()

            else:
                log.error(
                    'delete: account/role {}/{} is not allowed to do this'.format(
                        account.username, account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'delete: character id \'{}\' or account \'{}\' not found'.format(
                    self.url['id'], self.request.authenticated_userid))
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

            accountQuery = self.request.dbsession.query(Account)
            account = accountQuery.filter(Account.username == self.request.authenticated_userid).one()

            character_list = []
            for character in characters:
                #if they're an admin they can see everything
                if account.role == 3:
                    get_data = {
                        'accountId' : character.accountId,
                        'name'      : character.name,
                        'exp'       : character.exp,
                        'area'      : character.area,
                        'created'   : character.created,
                        'updated'   : character.updated,
                    }
                    character_list.append(get_data)
                else:
                    get_data = {
                        'accountId' : character.accountId,
                        'name'      : character.name
                    }
                    character_list.append(get_data)

            response = Response(json=character_list, content_type='application/json')

        except NoResultFound:
            log.error('get: could not retrieve any characters')
            raise HTTPNotFound

        return response

#Govern calls to an item on a character /character/{id}/item/{id}
@set_authorized
@view_defaults(route_name='character_item', renderer='json')
class CharacterItemViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            accountQuery = self.request.dbsession.query(Account)
            account = accountQuery.filter(Account.username == self.request.authenticated_userid).one()

            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['charId']).one()

            #if they own it or they're an admin
            if character.accountId == account.username or account.role == 3:

                item_query = self.request.dbsession.query(Inventory)
                item = item_query.filter(Inventory.id == self.url['itemId']).one()

                if character.id == item.characterId:
                    log.info(
                        'get: item {}/{} of character/id {}/{}'.format(
                            item.blueprintId, item.id, character.name, character.id))
                else:
                    log.error(
                        'update: item id \'{}\' not associated with char id \'{}\''.format(
                            self.url['itemId'],self.url['charId']))
                    raise HTTPClientError
            else:
                log.error(
                    'update: character id {} is not associated with account {}'.format(
                        self.url['charId'], account.username))

                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'get: item id \'{}\', char id \'{}\', or account \'{}\' not found'.format(
                    self.url['itemId'], self.url['charId'], self.request.authenticated_userid))
            raise HTTPNotFound

        return item

    #This method will be locked down since we should not allow any of this to be editable
    #Only admins or nwn (via db) should be able to create new characters or edit new characters
    @view_config(request_method='PUT')
    def update(self):
        try:
            accountQuery = self.request.dbsession.query(Account)
            account = accountQuery.filter(Account.username == self.request.authenticated_userid).one()

            #if they own it or they're an admin
            if account.role == 3:
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
                        'update: item/amount {}/{} from character/id {}/{} with new data {}'.format(
                            item.blueprintId, item.amount, character.name, character.id, put_data['amount']))

                    if amount:
                        item.amount = amount
                else:
                    log.error(
                        'update: item id \'{}\' not associated with char id \'{}\''.format(
                            self.url['itemId'], self.url['charId']))
                    raise HTTPClientError

            else:
                'update: account/role {}/{} is not allowed to do this'.format(
                    account.username, account.role)
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'update: item id \'{}\' or char id \'{}\' not found'.format(
                    self.url['itemId'], self.url['charId']))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.body))
            raise HTTPClientError

        return item

    #This method will be locked down since we should not allow any of this to be editable
    #Only admin server or nwn (via db) should be able to delete characters
    @view_config(request_method='DELETE')
    def delete(self):
        try:
            accountQuery = self.request.dbsession.query(Account)
            account = accountQuery.filter(Account.username == self.request.authenticated_userid).one()

            #if they own it or they're an admin
            if account.role == 3:
                #Maybe remove the char lookup?
                query = self.request.dbsession.query(Character)
                character = query.filter(Character.id == self.url['charId']).one()

                item_query = self.request.dbsession.query(Inventory)
                item = item_query.filter(Inventory.id == self.url['itemId']).one()

                if character.id == item.characterId:
                    item_query.filter(Inventory.id == self.url['itemId']).delete()
                    log.info(
                        'delete: item/amount {}/{} from character/id {}/{}'.format(
                            item.blueprintId, item.amount, character.name, character.id))

                    #we should return the full list of characters for a delete attempt
                    inv_query = self.request.dbsession.query(Inventory)
                    inventory = inv_query.filter(Inventory.characterId == self.url['charId']).all()

                else:
                    log.error(
                        'update: item id \'{}\' not associated with char id \'{}\''.format(
                            self.url['itemId'], self.url['charId']))
                    raise HTTPClientError

            else:
                log.error(
                    'delete: account/role {}/{} is not allowed to do this'.format(
                        account.username, account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'get: item id \'{}\' or char id \'{}\' not found'.format(
                    self.url['itemId'], self.url['charId']))
            raise HTTPNotFound

        return inventory

#Govern calls to a character's inventory /character/{id}/inventory
@set_authorized
@view_defaults(route_name='character_inventory', renderer='json')
class CharacterInventoryViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            accountQuery = self.request.dbsession.query(Account)
            account = accountQuery.filter(Account.username == self.request.authenticated_userid).one()

            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()

            #if they own it or they're an admin
            if character.accountId == account.username or account.role == 3:

                inv_query = self.request.dbsession.query(Inventory)
                inventory = inv_query.filter(Inventory.characterId == self.url['id']).all()
                log.info(
                    'get: inventory of character/id {}/{}'.format(character.name, character.id))
            else:
                log.error(
                    'update: character id {} is not associated with account {}'.format(
                        self.url['id'], account.username))

                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'get: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        return inventory

    #This method will be locked down since we should not allow any of this to be editable
    #Only admin server or nwn (via db) should be able to create items
    @view_config(request_method='POST')
    def create(self):
        try:
            accountQuery = self.request.dbsession.query(Account)
            account = accountQuery.filter(Account.username == self.request.authenticated_userid).one()

            #if they own it or they're an admin
            if account.role == 3:
                query = self.request.dbsession.query(Character)
                character = query.filter(Character.id == self.url['id']).one()

                schema = InventoryCreateSchema()
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
                    'create: item/amount {}/{} from character/id {}/{}'.format(
                        newItem.blueprintId, newItem.amount, character.name, character.id))
            else:
                log.error(
                    'create: account/role {}/{} is not allowed to do this'.format(
                        account.username, account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'update: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.POST))
            raise HTTPClientError

        return newItem
