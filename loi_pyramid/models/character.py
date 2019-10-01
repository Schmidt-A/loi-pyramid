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
    
    id = Column(Integer, primary_key=True, info={'access': 'public'})
    accountId = Column(Integer, ForeignKey('accounts.username'), info={'access': 'public'})
    name = Column(String, info={'access': 'public'})
    exp = Column(Integer, default=0, info={'access': 'private'})
    area = Column(String, default='Dreyen Inn', info={'access': 'private'})

    # Is it worth doing backpopulation? It's only useful for chained deletes
    account = relationship('Account', back_populates='characters')
    items = relationship('Item', back_populates='character')
