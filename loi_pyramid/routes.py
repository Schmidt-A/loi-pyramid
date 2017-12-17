def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('login_stub', '/login_stub')

    config.add_route('characters', '/characters')
    config.add_route('character', '/character/{id}')
    config.add_route('character_reputation', '/character/{id}/reputations')
    config.add_route('character_inventory', '/character/{id}/inventory')
    config.add_route('character_item', '/character/{charId}/inventory/{itemId}')
