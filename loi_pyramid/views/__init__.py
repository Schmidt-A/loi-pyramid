import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPClientError, HTTPForbidden, HTTPUnauthorized, HTTPInternalServerError
from pyramid.response import Response

from sqlalchemy.inspection import inspect
from sqlalchemy.orm.exc import NoResultFound

from ..models import Account

log = logging.getLogger(__name__)


class BaseView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # GET /resources/{id}
    def get_one(self, model):
        try:
            primary_key = inspect(model).primary_key[0].key
            if primary_key in self.request.matchdict:
                path_value = self.request.matchdict[primary_key]
            else:
                path_value = self.request.matchdict[model.__primary__]

            foreign_key = model.get_foreign_key_by(model, Account)

            result_query = self.request.dbsession.query(model)
            result = result_query.filter(
                getattr(model, primary_key) == path_value).one()

            log.warning(
                'get: {} {}'.format(model.__tablename__, path_value))

            owned = False
            if foreign_key:
                foreign_value = getattr(result, foreign_key.parent.name, None)
                if foreign_value == self.request.account.username:
                    owned = True
            # this is still too hacky
            elif getattr(result, 'username', None) == self.request.account.username:
                owned = True

            get_data = {}
            if owned or self.request.account.is_admin():
                get_data = result.owned_payload
            else:
                #TODO: handle the forbidden properly
                get_data = result.public_payload

            log.warning('get: returned {}'.format(get_data))
            response = Response(json=get_data, content_type='application/json')

        except NoResultFound:
            log.warning(
                'get: {} \'{}\' not found'.format(
                    model.__tablename__,
                    path_value))
            raise HTTPNotFound

        return response

    # GET /resources
    def get_all(self, model):
        try:
            limit = 10
            offset = 0

            try:
                if self.request.GET.getone('limit') > 0 and self.request.GET.getone('limit') < 101:
                    limit = self.request.GET.getone('limit')
                if self.request.GET.getone('offset') > -1:
                    offset = self.request.GET.getone('offset')
            except BaseException:
                log.warning(
                    'get: defaults used for limit and/or offset {}'.format(self.request.GET))
                pass

            result_query = self.request.dbsession.query(model).limit(limit).offset(offset)
            results = result_query.all()

            total_query = self.request.dbsession.query(model)
            total = total_query.count()

            log.warning(
                'get_all: {} queried by limit {} and offset {}'.format(
                    model.__tablename__, limit, offset))

            if offset + limit > total:
                offset = total
            else:
                offset += limit

            get_all_data = {
                'total': total,
                'offset': offset,
                model.__tablename__: []}
            for result in results:

                # if they're an admin they can see everything
                # need to add if owned
                if self.request.account.is_admin():
                    get_all_data[model.__tablename__].append(
                        result.owned_payload)
                else:
                    if model.__public__(model):
                        get_all_data[model.__tablename__].append(result.public_payload)

            log.warning('get_all: returned {}'.format(get_all_data))
            response = Response(
                json=get_all_data,
                content_type='application/json')

        except NoResultFound:
            log.error('get_all: could not retrieve any {}').format(
                model.__tablename__)

            get_all_data = []
            response = Response(
                json=get_all_data,
                content_type='application/json')

        return response

    # GET /resources/{id}/items
    def get_all_by_one(self, model_by, model_get):
        try:
            limit = 10
            offset = 0

            by_primary_key = inspect(model_by).primary_key[0].key
            if by_primary_key in self.request.matchdict:
                by_path_value = self.request.matchdict[by_primary_key]
            else:
                by_path_value = self.request.matchdict[model_by.__primary__]

            get_foreign_key = model_get.get_foreign_key_by(model_get, model_by)
            by_foreign_key = model_by.get_foreign_key_by(model_by, Account)

            if not get_foreign_key:
                log.error(
                    'get_all_by_one: {} and {} are not linked by foreign key'.format(
                        model_get.__tablename__,
                        model_by.__tablename__))
                raise HTTPInternalServerError

            try:
                if self.request.GET.getone('limit') > 0 and self.request.GET.getone('limit') < 101:
                    limit = self.request.GET.getone('limit')
                if self.request.GET.getone('offset') > -1:
                    offset = self.request.GET.getone('offset')
            except BaseException:
                log.warning(
                    'get_all_by_one: defaults used for limit and/or offset {}'.format(self.request.GET))
                pass

            # only doing this because otherwise the NoResultFound won't throw - might refactor by making it an if character returned
            # TODO: should probably use effective principles or authenticated
            # userid
            try:
                filter_query = self.request.dbsession.query(model_by)
                filter_result = filter_query.filter(
                    getattr(model_by, by_primary_key) == by_path_value).one()

            except NoResultFound:
                log.warning(
                    'get_all_by_one: {} \'{}\' not found'.format(
                        model_by.__tablename__, by_path_value))
                raise HTTPNotFound

            results_query = self.request.dbsession.query(model_get)
            results_query = results_query.filter(
                getattr(model_get, get_foreign_key.parent.name) == by_path_value)
            results_query = results_query.limit(limit).offset(offset)
            results = results_query.all()

            total_query = self.request.dbsession.query(model_get)
            total = total_query.filter(
                getattr(model_get, get_foreign_key.parent.name) == by_path_value).count()

            log.warning('get_all_by_one: {} of {}: {} by limit {} and offset {}'.format(
                model_get.__tablename__, model_by.__tablename__, by_path_value, limit, offset))

            if offset + limit > total:
                offset = total
            else:
                offset += limit

            # I dislike this owned nesting
            owned = False
            if by_foreign_key:
                by_foreign_value = getattr(filter_result, by_foreign_key.parent.name, None)
                if by_foreign_value == self.request.account.username:
                    owned = True
            # this is still too hacky
            elif getattr(filter_result, 'username', None) == self.request.account.username:
                owned = True

            if not (owned or self.request.account.is_admin()) and not model_get.__public__(model_get):
                log.warning(
                    'get_all_by_one: {} by {} is not allowed to be accesed by account {}'.format(
                        model_get.__tablename__,
                        by_path_value,
                        self.request.account.username))
                raise HTTPForbidden

            get_all_data = {
                'total': total,
                'offset': offset,
                model_get.__tablename__: []}
            for result in results:

                get_foreign_value = getattr(result, get_foreign_key.parent.name, None)
                if get_foreign_value  == self.request.account.username:
                    owned = True

                if owned or self.request.account.is_admin():
                    get_all_data[model_get.__tablename__].append(
                        result.owned_payload)
                else:
                    if model_get.__public__(model_get):
                        get_all_data[model_get.__tablename__].append(result.public_payload)

            log.warning(
                'get_all_by_one: returned {} from {}'.format(
                    get_all_data, by_path_value))
            response = Response(
                json=get_all_data,
                content_type='application/json')

        except NoResultFound:
            log.warning(
                'get_all_by_one: no {} found with {} {}'.format(
                    model_get.__tablename__,
                    model_by.__tablename__,
                    by_path_value))
            get_all_data = []
            response = Response(
                json=get_all_data,
                content_type='application/json')

        return response

    # GET /resources/{id}/items/{id}
    def get_one_by_one(self, model_by, model_get):
        try:
            by_primary_key = inspect(model_by).primary_key[0].key
            get_primary_key = inspect(model_get).primary_key[0].key

            if by_primary_key in self.request.matchdict:
                by_path_value = self.request.matchdict[by_primary_key]
            else:
                by_path_value = self.request.matchdict[model_by.__primary__]
            if get_primary_key in self.request.matchdict:
                get_path_value = self.request.matchdict[get_primary_key]
            else:
                get_path_value = self.request.matchdict[model_get.__primary__]

            get_foreign_key = model_get.get_foreign_key_by(model_get, model_by)
            by_foreign_key = model_by.get_foreign_key_by(model_by, Account)

            if not get_foreign_key:
                log.error(
                    'get_one_by_one: {} and {} are not linked by foreign key'.format(
                        model_get.__tablename__,
                        model_by.__tablename__))
                raise HTTPInternalServerError

            # only doing this because otherwise the NoResultFound won't throw - might refactor by making it an if character returned
            # TODO: should probably use effective principles or authenticated
            # userid
            filter_query = self.request.dbsession.query(model_by)
            filter_result = filter_query.filter(
                getattr(model_by, by_primary_key) == by_path_value).one()

            result_query = self.request.dbsession.query(model_get)
            result = result_query.filter(
                getattr(model_get, get_primary_key) == get_path_value).one()

            log.warning(
                'get_one_by_one: {}: {} of {}: {}'.format(
                    model_get.__tablename__,
                    get_path_value,
                    model_by.__tablename__,
                    by_path_value))

            get_foreign_value = getattr(result, get_foreign_key.parent.name, None)
            by_primary_value = getattr(filter_result, by_primary_key, None)

            if get_foreign_value != by_primary_value:
                log.warning(
                    'get_one_by_one: {} {} is not associated with {} {}'.format(
                        model_get.__tablename__,
                        get_path_value,
                        model_by.__tablename__,
                        by_path_value))
                raise HTTPClientError

            owned = False
            if get_foreign_value == self.request.account.username:
                owned = True
            elif by_foreign_key:
                by_foreign_value = getattr(filter_result, by_foreign_key.parent.name, None)
                if by_foreign_value == self.request.account.username:
                    owned = True
            # this is still too hacky
            elif getattr(result, 'username', None) == self.request.account.username:
                owned = True

            get_data = {}
            if owned or self.request.account.is_admin():
                get_data = result.owned_payload
            else:
                get_data = result.public_payload
                if not get_data:
                    log.warning(
                        'get_one_by_one: {} {} is not allowed to be accesed by account {}'.format(
                            model_get.__tablename__,
                            get_path_value,
                            self.request.account.username))
                    raise HTTPForbidden

            log.warning(
                'get_one_by_one: returned {} from {}'.format(
                    get_data, by_path_value))
            response = Response(json=get_data, content_type='application/json')

        except NoResultFound:
            log.warning(
                'get_one_by_one: no {} {} with {} {} found'.format(
                    model_get.__tablename__,
                    get_path_value,
                    model_by.__tablename__,
                    by_path_value))
            raise HTTPNotFound

        return response

    # admin DELETE /resources/{id}
    def admin_delete_one(self, model):
        try:
            primary_key = inspect(model).primary_key[0].key
            if primary_key in self.request.matchdict:
                path_value = self.request.matchdict[primary_key]
            else:
                path_value = self.request.matchdict[model.__primary__]

            if not self.request.account.is_admin():
                log.warning(
                    'admin_delete_one: {} {} is not allowed to be accesed by account {}'.format(
                        model.__tablename__,
                        path_value,
                        self.request.account.username))
                raise HTTPForbidden

            delete_query = self.request.dbsession.query(model)
            delete_result = delete_query.filter(
                getattr(model, primary_key) == path_value).one()

            log.warning(
                'admin_delete_one: {} {}'.format(model.__tablename__, path_value))

            delete_query.filter(
                    getattr(model, primary_key) == path_value).delete()

            limit = 10
            position = getattr(delete_result, primary_key)
            offset = position-limit if position-limit > 0 else 0

            results_query = self.request.dbsession.query(model)
            results_query = results_query.limit(limit).offset(offset)
            results = results_query.all()

            total_query = self.request.dbsession.query(model)
            total = total_query.count()

            get_all_data = {
                'total': total,
                'offset': offset,
                model.__tablename__: []}
            for result in results:
                get_all_data[model.__tablename__].append(result.owned_payload)

            log.warning('admin_delete_one: deleted {} {}'.format(
                    model.__tablename__, path_value))
            response = Response(json=get_all_data, content_type='application/json')

        except NoResultFound:
            log.warning(
                'admin_delete_one: {} \'{}\' not found'.format(
                    model.__tablename__,
                    path_value))
            raise HTTPNotFound

        return response

    # admin DELETE /resources/{id}/items/{id} 
    def admin_delete_one_by_one(self, model_by, model_get):
        try:
            by_primary_key = inspect(model_by).primary_key[0].key
            get_primary_key = inspect(model_get).primary_key[0].key

            if by_primary_key in self.request.matchdict:
                by_path_value = self.request.matchdict[by_primary_key]
            else:
                by_path_value = self.request.matchdict[model_by.__primary__]
            if get_primary_key in self.request.matchdict:
                get_path_value = self.request.matchdict[get_primary_key]
            else:
                get_path_value = self.request.matchdict[model_get.__primary__]

            if not self.request.account.is_admin():
                log.warning(
                    'admin_delete_one_by_one: {} {} is not allowed to be accesed by account {}'.format(
                        model_get.__tablename__,
                        get_path_value,
                        self.request.account.username))
                raise HTTPForbidden

            get_foreign_key = model_get.get_foreign_key_by(model_get, model_by)

            if not get_foreign_key:
                log.error(
                    'admin_delete_one_by_one: {} and {} are not linked by foreign key'.format(
                        model_get.__tablename__,
                        model_by.__tablename__))
                raise HTTPInternalServerError

            # only doing this because otherwise the NoResultFound won't throw - might refactor by making it an if character returned
            # TODO: should probably use effective principles or authenticated
            # userid
            filter_query = self.request.dbsession.query(model_by)
            filter_result = filter_query.filter(
                getattr(model_by, by_primary_key) == by_path_value).one()

            delete_query = self.request.dbsession.query(model_get)
            delete_result = delete_query.filter(
                getattr(model_get, get_primary_key) == get_path_value).one()

            log.warning(
                'admin_delete_one_by_one: {}: {} of {}: {}'.format(
                    model_get.__tablename__,
                    get_path_value,
                    model_by.__tablename__,
                    by_path_value))

            get_foreign_value = getattr(delete_result, get_foreign_key.parent.name, None)
            by_primary_value = getattr(filter_result, by_primary_key, None)

            if get_foreign_value != by_primary_value:
                log.warning(
                    'admin_delete_one_by_one: {} {} is not associated with {} {}'.format(
                        model_get.__tablename__,
                        get_path_value,
                        model_by.__tablename__,
                        by_path_value))
                raise HTTPClientError

            delete_query.filter(
                    getattr(model_get, get_primary_key) == get_path_value).delete()

            limit = 10
            position = getattr(delete_result, get_primary_key)
            offset = position-limit if position-limit > 0 else 0

            results_query = self.request.dbsession.query(model_get)
            results_query = results_query.filter(
                getattr(model_get, get_foreign_key.parent.name) == by_path_value)
            results_query = results_query.limit(limit).offset(offset)
            results = results_query.all()

            total_query = self.request.dbsession.query(model_get)
            total = total_query.filter(
                getattr(model_get, get_foreign_key.parent.name) == by_path_value).count()

            get_all_data = {
                'total': total,
                'offset': offset,
                model_get.__tablename__: []}
            for result in results:
                get_all_data[model_get.__tablename__].append(result.owned_payload)

            log.warning(
                'admin_delete_one_by_one: deleted {} {}'.format(
                    model_get.__tablename__, get_path_value))
            response = Response(json=get_all_data, content_type='application/json')

        except NoResultFound:
            log.warning(
                'admin_delete_one_by_one: no {} {} with {} {} found'.format(
                    model_get.__tablename__,
                    get_path_value,
                    model_by.__tablename__,
                    by_path_value))
            raise HTTPNotFound

        return response
