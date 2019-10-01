import logging
from datetime import datetime

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from . import BaseView
from ..models import Character, Item, Account, Action
from ..schemas import CharacterAdminUpdate, ItemAdminUpdate, ItemAdminCreate, Invalid


log = logging.getLogger(__name__)

# Govern calls to a single character object /characters/{id}
@view_defaults(route_name='character', renderer='json')
class CharacterViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_one(Character)

    # This method will be locked down since we should not allow any of this to be editable
    # Only admins or nwn (via db) should be able to create new characters or edit new characters
    # I'm not going to expose a new api for making new characters, that should
    # be done by NWN only
    @view_config(request_method='PUT', permission='admin')
    def update(self):
        try:
            # if they're an admin they can do everything
            if self.request.account.is_admin():
                query = self.request.dbsession.query(Character)
                character = query.filter(
                    Character.id == self.request.matchdict['charId']).one()

                schema = CharacterAdminUpdate()
                put_data = schema.deserialize(self.request.body)
                exp = put_data['exp']
                area = put_data['area']

                # should we allow this api to update all more things like
                # transferring account ownership?
                if exp:
                    character.exp = exp
                if area:
                    character.area = area
                character.updated = str(datetime.now())

                response = Response(
                    json=character.owned_payload,
                    content_type='application/json')

                log.info(
                    'update: character/id {}/{} with new data {}'.format(
                        character.name, character.id, [
                            put_data['exp'], put_data['area']]))

            else:
                log.warning(
                    'update: account/role {}/{} is not allowed to do this'.format(
                        self.request.account.username,
                        self.request.account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error('update: character id \'{}\' or account \'{}\' not found'.format(
                self.request.matchdict['charId'], self.request.authenticated_userid))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.body))
            raise HTTPClientError

        return response

    # This method will almost certainly be locked down since we should not allow any of this to be editable
    # Only admin server or nwn (via db) should be able to delete characters
    @view_config(request_method='DELETE', permission='admin')
    def delete(self):
        return self.admin_delete_one(Character)

# Govern calls to all character objects /characters
@view_defaults(route_name='characters', renderer='json')
class CharactersViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all(Character)

# Govern calls to an item on a character /characters/{id}/items/{id}
@view_defaults(route_name='character_item', renderer='json')
class CharacterItemViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_one_by_one(Character, Item)

    # This method will be locked down since we should not allow any of this to be editable
    # Only admins or nwn (via db) should be able to create new characters or
    # edit new characters
    @view_config(request_method='PUT', permission='admin')
    def update(self):
        try:
            # if they own it or they're an admin
            if self.request.account.is_admin():
                # Maybe remove the char lookup?
                query = self.request.dbsession.query(Character)
                character = query.filter(
                    Character.id == self.request.matchdict['charId']).one()

                item_query = self.request.dbsession.query(Item)
                item = item_query.filter(
                    Item.id == self.request.matchdict['itemId']).one()

                schema = ItemAdminUpdate()
                put_data = schema.deserialize(self.request.body)
                amount = put_data['amount']

                if character.id == item.characterId:
                    log.info(
                        'update: item/amount {}/{} from character/id {}/{} with new data {}'.format(
                            item.resref,
                            item.amount,
                            character.name,
                            character.id,
                            put_data['amount']))

                    # should we allow this api to update all more things like
                    # transferring api ownership?
                    if amount:
                        item.amount = amount
                    item.updated = str(datetime.now())

                    response = Response(
                        json=item.owned_payload,
                        content_type='application/json')

                else:
                    log.warning(
                        'update: item id \'{}\' not associated with char id \'{}\''.format(
                            self.request.matchdict['itemId'],
                            self.request.matchdict['charId']))
                    raise HTTPClientError

            else:
                log.warning(
                    'update: account/role {}/{} is not allowed to do this'.format(
                        self.request.account.username,
                        self.request.account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error('update: item id \'{}\' or char id \'{}\' not found'.format(
                self.request.matchdict['itemId'], self.request.matchdict['charId']))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.body))
            raise HTTPClientError

        return response

    # This method will be locked down since we should not allow any of this to be editable
    # Only admin server or nwn (via db) should be able to delete characters
    @view_config(request_method='DELETE', permission='admin')
    def delete(self):
        return self.admin_delete_one_by_one(Character, Item)

# Govern calls to a character's items /characters/{id}/items
@view_defaults(route_name='character_items', renderer='json')
class CharacterItemsViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all_by_one(Character, Item)

    # This method will be locked down since we should not allow any of this to be editable
    # Only admin server or nwn (via db) should be able to create items
    @view_config(request_method='POST', permission='admin')
    def create(self):
        try:
            # if they own it or they're an admin
            if self.request.account.is_admin():
                query = self.request.dbsession.query(Character)
                character = query.filter(
                    Character.id == self.request.matchdict['charId']).one()

                schema = ItemAdminCreate()
                post_data = schema.deserialize(self.request.body)

                # TODO: Create a way to check if the character already owns an
                # item of the same resref
                characterId = character.id
                resref = post_data['resref']
                amount = post_data['amount']

                newItem = Item(
                    characterId=characterId,
                    resref=resref,
                    amount=amount)
                self.request.dbsession.add(newItem)

                log.info('create: item/amount {}/{} from character/id {}/{}'.format(
                    newItem.resref, newItem.amount, character.name, character.id))

                response = Response(
                    json=newItem.owned_payload,
                    content_type='application/json')

            else:
                log.warning(
                    'create: account/role {}/{} is not allowed to do this'.format(
                        self.request.account.username,
                        self.request.account.role))
                raise HTTPForbidden

        except NoResultFound:
            log.error(
                'update: character id \'{}\' not found'.format(
                    self.request.matchdict['charId']))
            raise HTTPNotFound

        except Invalid:
            log.error(
                'update: could not deserialize {}'.format(self.request.body))
            raise HTTPClientError

        return response


# Govern calls to an action of a character /characters/{id}/actions/{id}
@view_defaults(route_name='character_action', renderer='json')
class CharacterActionViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_one_by_one(Character, Action)

    @view_config(request_method='DELETE', permission='admin')
    def delete(self):
        return self.admin_delete_one_by_one(Character, Action)


# Govern calls to a character's actions /characters/{id}/actions
@view_defaults(route_name='character_actions', renderer='json')
class CharacterActionsViews(BaseView):

    @view_config(request_method='GET')
    def get(self):
        return self.get_all_by_one(Character, Action)
