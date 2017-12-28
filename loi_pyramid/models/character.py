# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base


class Character(Base):
    __tablename__ = 'characters'
    id          = Column(Integer, primary_key=True)
    accountId   = Column(String)
    name        = Column(String)
    exp         = Column(Integer)
    area        = Column(String)

    def owned_payload(self):
        return {
            'id'        : self.id,
            'accountId' : self.accountId,
            'name'      : self.name,
            'exp'       : self.exp,
            'area'      : self.area,
            'created'   : self.created,
            'updated'   : self.updated
        }

    def public_payload(self):
        return {
            'id'        : self.id,
            'accountId' : self.accountId,
            'name'      : self.name,
            'created'   : self.created,
            'updated'   : self.updated
        }
