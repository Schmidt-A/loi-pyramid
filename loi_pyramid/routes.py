def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('login_stub', '/login_stub')

    config.add_route('characters', '/characters')
    config.add_route('character', '/character/{id}')

    config.add_route('character_items', '/character/{id}/items')
    config.add_route('character_item', '/character/{charId}/item/{itemId}')
    config.add_route('character_actions', '/character/{id}/actions')
    config.add_route('character_action', '/character/{charId}/action/{actionId}')

    config.add_route('account', '/account/{username}')
    config.add_route('accounts', '/accounts')
    config.add_route('account_characters', '/account/{username}/characters')

    config.add_route('recipe', '/recipe/{blueprint}')
    config.add_route('recipes', '/recipes')

    config.add_route('ingredient', '/ingredient/{material}')
    config.add_route('ingredients', '/ingredients')
