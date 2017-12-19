import bcrypt

from .models import Account

def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')

def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)

def role_lookup(username, request):
    query = self.request.dbsession.query(Account)
    account = query.filter(Account.username == username).one()

    roles = account.role
    return roles
