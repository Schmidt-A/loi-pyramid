# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base


class Item(Base):
    __tablename__ = 'items'
    id          = Column(Integer, primary_key=True)
    characterId = Column(Integer)
    blueprintId = Column(String)
    amount      = Column(Integer)

    def owned_payload(self):
        return {
            'id'            : self.id,
            'characterId'   : self.characterId,
            'blueprintId'   : self.blueprintId,
            'amount'        : self.amount,
            'created'       : self.created,
            'updated'       : self.updated
        }
