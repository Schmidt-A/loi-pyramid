from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from .utils.security import role_lookup, get_account, Root

def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')

    authn_policy = AuthTktAuthenticationPolicy(
        settings['loi.secret'], callback=role_lookup, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(Root)
    config.set_default_permission('authenticated')
    config.add_request_method(get_account, 'account', reify=True)

    config.scan()

    return config.make_wsgi_app()
