# flake8: noqa
import logging

from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    Boolean
)
from sqlalchemy.orm import relationship

from .meta import Base

log = logging.getLogger(__name__)

# TODO: Change password to binary because sqlite doesn't support
class Account(Base):
    __tablename__ = 'accounts'
    __primary__ = 'username'

    username = Column(String, primary_key=True, info={'access': 'public'})
    password = Column(LargeBinary, info={'access': 'secret'})
    cdkey = Column(String, info={'access': 'private'})
    ip = Column(String, info={'access': 'private'})
    role = Column(Integer, default=1, info={'access': 'public'})
    actions = Column(Integer, default=0, info={'access': 'private'})
    approved = Column(Integer, default=0, info={'access': 'public'})
    banned = Column(Integer, default=0, info={'access': 'public'})

    # Is it worth doing backpopulation? It's only useful for chained deletes
    characters = relationship('Character', back_populates='account')
    
    def is_owner(self, character):
        return self.username == character.accountId

    def is_admin(self):
        return self.role > 2
