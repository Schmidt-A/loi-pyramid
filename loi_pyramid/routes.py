

def includeme(config):
    #including CORS
    config.include('.utils.cors')
    config.add_cors_preflight_handler()

    config.add_static_view(name='static', path='loi_pyramid:static', cache_max_age=3600)

    config.add_route('login_stub', '/login_stub')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('characters', '/characters')
    config.add_route('character', '/characters/{id}')

    config.add_route('character_items', '/characters/{id}/items')
    config.add_route('character_item', '/characters/{charId}/item/{itemId}')
    config.add_route('character_actions', '/characters/{id}/actions')
    config.add_route('character_action', '/characters/{charId}/action/{actionId}')

    config.add_route('account', '/accounts/{username}')
    config.add_route('accounts', '/accounts')
    config.add_route('account_characters', '/accounts/{username}/characters')

    config.add_route('recipe', '/recipe/{blueprint}')
    config.add_route('recipes', '/recipes')

    config.add_route('ingredient', '/ingredient/{material}')
    config.add_route('ingredients', '/ingredients')
