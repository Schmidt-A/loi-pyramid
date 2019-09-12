from pyramid.view import view_config

from . import BaseView


class StubViews(BaseView):

    @view_config(route_name='login_stub', request_method='GET', renderer='../templates/login_stub.jinja2', permission='login')
    def get(self):
        return {}
