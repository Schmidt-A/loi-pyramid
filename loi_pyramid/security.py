import bcrypt
from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    Authenticated,
    Deny,
    Everyone,
)
from .models import Account


def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')

def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)

def role_lookup(username, request):
    query = request.dbsession.query(Account)
    account = query.filter(Account.username == username).one()

    role = []
    if account.role == 3:
        role.append('g:admin')

    return role

def get_account(request):
    query = request.dbsession.query(Account)
    account = query.filter(Account.username == request.authenticated_userid).one()

    return account

class LoIACL(object):
    __acl__ = [
        (Allow, Everyone, 'login'),
        (Allow, Authenticated, 'authenticated'),
        (Allow, 'group:admin', 'admin')
    ]

    def __init__(self, request):
        pass