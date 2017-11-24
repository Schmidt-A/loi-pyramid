from pyramid.httpexceptions import HTTPNotFound

from pyramid.view import view_config, view_defaults

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from . import BaseView

from ..models import Character

@view_defaults(route_name='character', renderer='json')
class CharacterViews(BaseView):

    #@authorized
    @view_config(request_method='GET')
    def get(self):
        try:
            query = self.request.dbsession.query(Character)
            character = query.filter(Character.id == self.url['id']).one()
        except NoResultFound:
            raise HTTPNotFound

        return character.as_dict()
