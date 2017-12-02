from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from .security import groupfinder


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('.models')
    config.include('.routes')

    authn_policy = AuthTktAuthenticationPolicy(
        settings['loi.secret'], callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.scan()

    return config.make_wsgi_app()
