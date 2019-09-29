# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from .meta import Base


class Character(Base):
    __tablename__ = 'characters'
    __primary__ = 'charId'
    id          = Column(Integer, primary_key=True)
    accountId   = Column(Integer, ForeignKey('accounts.username'))
    name        = Column(String)
    exp         = Column(Integer)
    area        = Column(String)

    #Is it worth doing backpopulation? It's only useful for chained deletes
    account     = relationship('Account', back_populates='characters')
    items       = relationship('Item', back_populates='character')

    @property
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

    @property
    def public_payload(self):
        return {
            'id'        : self.id,
            'accountId' : self.accountId,
            'name'      : self.name,
            'created'   : self.created,
            'updated'   : self.updated
        }
