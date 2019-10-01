# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from .meta import Base


class Item(Base):
    __tablename__ = 'items'
    __table_args__ = {'info':{'access': 'private'}}
    __primary__ = 'itemId'

    id = Column(Integer, primary_key=True, info={'access': 'public'})
    characterId = Column(Integer, ForeignKey('characters.id'), info={'access': 'private'})
    resref = Column(String, info={'access': 'private'})
    amount = Column(Integer, info={'access': 'private'})

    # Is it worth doing backpopulation? It's only useful for chained deletes
    character = relationship('Character', back_populates='items')
