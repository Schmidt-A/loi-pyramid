# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    Boolean
)

from .meta import Base


# TODO: Change password to binary because sqlite doesn't support
class Account(Base):
    __tablename__   = 'accounts'
    username    = Column(String, primary_key=True)
    password    = Column(LargeBinary)
    cdkey       = Column(String)
    ip          = Column(String)
    role        = Column(Integer)
    actions     = Column(Integer)
    approved    = Column(Integer)
    banned      = Column(Integer)

    def owned_payload(self):
        return {
            'username'  : self.username,
            'cdkey'     : self.cdkey,
            'ip'        : self.ip,
            'role'      : self.role,
            'actions'   : self.actions,
            'approved'  : self.approved,
            'banned'    : self.banned,
            'created'   : self.created,
            'updated'   : self.updated
        }

    def public_payload(self):
        return {
            'username'  : self.username,
            'role'      : self.role,
            'approved'  : self.approved,
            'banned'    : self.banned,
            'created'   : self.created,
            'updated'   : self.updated
        }
