import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Character, Item, Account
from ..decorators import set_authorized
from ..schemas import CharacterAdminUpdate, ItemAdminUpdate, ItemAdminCreate, Invalid


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
                'get: character/id {}/{} by account {}'.format(
                    character.name, character.id, self.request.account.username))

            #if they own it or they're an admin
            #infuriatingly, unittest does not recognize the valid character.account relationship
            if self.request.account.is_owner(character) or self.request.account.is_admin():
                response = Response(json=character.owned_payload, content_type='application/json')

            else:
                response = Response(json=character.public_payload, content_type='application/json')

        except NoResultFound:
            log.error(
                'get: character id \'{}\' or account \'{}\' not found'.format(
                    self.url['id'], self.request.authenticated_userid))
            raise HTTPNotFound

        return response

    #This method will be locked down since we should not allow any of this to be editable
    #Only admins or nwn (via db) should be able to create new characters or edit new characters
    #I'm not going to expose a new api for making new characters, that should be done by NWN only
    @view_config(request_method='PUT')
    def update(self):
        try:
            #if they're an admin they can do everything
            if self.request.account.is_admin():
                query = self.request.dbsession.query(Character)
                character = query.filter(Character.id == self.url['id']).one()

                schema = CharacterAdminUpdate()
                put_data = schema.deserialize(self.request.body)
                exp         = put_data['exp']
                area        = put_data['area']

                #should we allow this api to update all more things like transferring account ownership?
                if exp:
                    character.exp = exp
                if area:
                    character.area = area
                character.set_updated()

                response = Response(json=character.owned_payload, content_type='application/json')

                log.info(
                    'update: character/id {}/{} with new data {}'.format(
                    character.name, character.id, [put_data['exp'], put_data['area']]))

            else:
                log.error(
                    'update: account/role {}/{} is not allowed to do this'.format(
                        self.request.account.username, self.request.account.role))
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

        return response


    #This method will almost certainly be locked down since we should not allow any of this to be editable
    #Only admin server or nwn (via db) should be able to delete characters
    @view_config(request_method='DELETE')
    def delete(self):
        try:
            #if they're an admin they can do everything
            if self.request.account.is_admin():
                query = self.request.dbsession.query(Character)

                #This dumb shit is only needed because we don't throw a not found error if it's not there
                query.filter(Character.id == self.url['id']).one()

                query.filter(Character.id == self.url['id']).delete()
                log.info(
                    'delete: character/id {}'.format(self.url['id']))

                #we should return the full list of characters for a delete attempt
                characters = self.request.dbsession.query(Character).all()

                get_all_data = []
                for character in characters:
                    get_all_data.append(character.owned_payload)

                response = Response(json=get_all_data, content_type='application/json')

            else:
                log.error(
                    'delete: account/role {}/{} is not allowed to do this'.format(
                        self.request.account.username, self.request.account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'delete: character id \'{}\' or account \'{}\' not found'.format(
                    self.url['id'], self.request.authenticated_userid))
            raise HTTPNotFound

        return response

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

            get_all_data = []
            for character in characters:
                #if they're an admin they can see everything
                if self.request.account.is_admin():
                    get_all_data.append(character.owned_payload)
                else:
                    get_all_data.append(character.public_payload)

            response = Response(json=get_all_data, content_type='application/json')

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
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['charId']).one()

            #if they own it or they're an admin
            #infuriatingly, unittest does not recognize the valid character.account relationship
            if self.request.account.is_owner(character) or self.request.account.is_admin():

                item_query = self.request.dbsession.query(Item)
                item = item_query.filter(Item.id == self.url['itemId']).one()

                if character.id == item.characterId:
                    log.info(
                        'get: item {}/{} of character/id {}/{}'.format(
                            item.resref, item.id, character.name, character.id))

                    response = Response(json=item.owned_payload, content_type='application/json')

                else:
                    log.error(
                        'update: item id \'{}\' not associated with char id \'{}\''.format(
                            self.url['itemId'], self.url['charId']))
                    raise HTTPClientError

            else:
                log.error(
                    'update: character id {} is not associated with account {}'.format(
                        self.url['charId'], self.request.account.username))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'get: item id \'{}\', char id \'{}\', or account \'{}\' not found'.format(
                    self.url['itemId'], self.url['charId'], self.request.authenticated_userid))
            raise HTTPNotFound

        return response

    #This method will be locked down since we should not allow any of this to be editable
    #Only admins or nwn (via db) should be able to create new characters or edit new characters
    @view_config(request_method='PUT')
    def update(self):
        try:
            #if they own it or they're an admin
            if self.request.account.is_admin():
                #Maybe remove the char lookup?
                query = self.request.dbsession.query(Character)
                character = query.filter(Character.id == self.url['charId']).one()

                item_query = self.request.dbsession.query(Item)
                item = item_query.filter(Item.id == self.url['itemId']).one()

                schema = ItemAdminUpdate()
                put_data = schema.deserialize(self.request.body)
                amount = put_data['amount']

                if character.id == item.characterId:
                    log.info(
                        'update: item/amount {}/{} from character/id {}/{} with new data {}'.format(
                            item.resref, item.amount, character.name, character.id, put_data['amount']))

                    #should we allow this api to update all more things like transferring api ownership?
                    if amount:
                        item.amount = amount
                    item.set_updated()

                    response = Response(json=item.owned_payload, content_type='application/json')

                else:
                    log.error(
                        'update: item id \'{}\' not associated with char id \'{}\''.format(
                            self.url['itemId'], self.url['charId']))
                    raise HTTPClientError

            else:
                'update: account/role {}/{} is not allowed to do this'.format(
                    self.request.account.username, self.request.account.role)
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

        return response

    #This method will be locked down since we should not allow any of this to be editable
    #Only admin server or nwn (via db) should be able to delete characters
    @view_config(request_method='DELETE')
    def delete(self):
        try:
            #if they own it or they're an admin
            if self.request.account.is_admin():
                #Maybe remove the char lookup?
                query = self.request.dbsession.query(Character)
                character = query.filter(Character.id == self.url['charId']).one()

                item_query = self.request.dbsession.query(Item)
                item = item_query.filter(Item.id == self.url['itemId']).one()

                if character.id == item.characterId:
                    item_query.filter(Item.id == self.url['itemId']).delete()
                    log.info(
                        'delete: item/amount {}/{} from character/id {}/{}'.format(
                            item.resref, item.amount, character.name, character.id))

                    #we should return the full list of characters for a delete attempt
                    inv_query = self.request.dbsession.query(Item)
                    items = inv_query.filter(Item.characterId == self.url['charId']).all()

                    get_all_data = []
                    for item in items:
                        get_all_data.append(item.owned_payload)

                    response = Response(json=get_all_data, content_type='application/json')

                else:
                    log.error(
                        'update: item id \'{}\' not associated with char id \'{}\''.format(
                            self.url['itemId'], self.url['charId']))
                    raise HTTPClientError

            else:
                log.error(
                    'delete: account/role {}/{} is not allowed to do this'.format(
                        self.request.account.username, self.request.account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'get: item id \'{}\' or char id \'{}\' not found'.format(
                    self.url['itemId'], self.url['charId']))
            raise HTTPNotFound

        return response

#Govern calls to a character's items /character/{id}/items
@set_authorized
@view_defaults(route_name='character_items', renderer='json')
class CharacterItemsViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()

            #if they own it or they're an admin
            #infuriatingly, unittest does not recognize the valid character.account relationship
            if self.request.account.is_owner(character) or self.request.account.is_admin():

                inv_query = self.request.dbsession.query(Item)
                items = inv_query.filter(Item.characterId == self.url['id']).all()
                log.info(
                    'get: items of character/id {}/{}'.format(character.name, character.id))

                get_all_data = []
                for item in items:
                    get_all_data.append(item.owned_payload)

                response = Response(json=get_all_data, content_type='application/json')

            else:
                log.error(
                    'update: character id {} is not associated with account {}'.format(
                        self.url['id'], self.request.account.username))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'get: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        return response

    #This method will be locked down since we should not allow any of this to be editable
    #Only admin server or nwn (via db) should be able to create items
    @view_config(request_method='POST')
    def create(self):
        try:
            #if they own it or they're an admin
            if self.request.account.is_admin():
                query = self.request.dbsession.query(Character)
                character = query.filter(Character.id == self.url['id']).one()

                schema = ItemAdminCreate()
                post_data = schema.deserialize(self.request.POST)

                #TODO: Create a way to check if the character already owns an item of the same resref
                characterId = character.id
                resref = post_data['resref']
                amount = post_data['amount']

                newItem = Item(
                    characterId = characterId,
                    resref = resref,
                    amount      = amount)
                self.request.dbsession.add(newItem)
                newItem.set_created()
                newItem.set_updated()

                log.info(
                    'create: item/amount {}/{} from character/id {}/{}'.format(
                        newItem.resref, newItem.amount, character.name, character.id))

                response = Response(json=newItem.owned_payload, content_type='application/json')

            else:
                log.error(
                    'create: account/role {}/{} is not allowed to do this'.format(
                        self.request.account.username, self.request.account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'update: character id \'{}\' not found'.format(self.url['id']))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.POST))
            raise HTTPClientError

        return response
