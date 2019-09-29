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
    __primary__ = 'itemId'
    id          = Column(Integer, primary_key=True)
    characterId = Column(Integer, ForeignKey('characters.id'))
    resref      = Column(String)
    amount      = Column(Integer)

    #Is it worth doing backpopulation? It's only useful for chained deletes
    character   = relationship('Character', back_populates='items')

    @property
    def owned_payload(self):
        return {
            'id'            : self.id,
            'characterId'   : self.characterId,
            'resref'        : self.resref,
            'amount'        : self.amount,
            'created'       : self.created,
            'updated'       : self.updated
        }
