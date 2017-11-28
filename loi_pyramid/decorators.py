def _needs_auth(val, attr):
    if attr.startswith('__') or hasattr(val, '_ignore_auth'):
        return False
    return True


def unauthed(func):
    func._ignore_auth = True
    return func


def authorized(view_func):
    def wrapped(*args, **kw):
        # TODO: auth checks
        print('I would require authorization in order to be called nicely')
        return view_func(*args, **kw)
    return wrapped


def set_authorized(cls):
    auth_funcs = []

    for attr, val in cls.__dict__.items():
        if _needs_auth(val, attr):
            auth_funcs.append((attr, val))

    for (attr, val) in auth_funcs:
        setattr(cls, attr, authorized(val))

    return cls
