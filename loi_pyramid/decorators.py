from .utils.decorator_functions import authorized, needs_auth

def no_auth(func):
    func._ignore_auth = True
    return func


def set_authorized(cls):
    auth_funcs = []

    for attr, val in cls.__dict__.items():
        if needs_auth(val, attr):
            auth_funcs.append((attr, val))

    for (attr, val) in auth_funcs:
        setattr(cls, attr, authorized(val))

    return cls


