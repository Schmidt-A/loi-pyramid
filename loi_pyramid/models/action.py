# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base


class Action(Base):
    __tablename__ = 'actions'
    id          = Column(Integer, primary_key=True)
    characterId = Column(Integer)
    amount      = Column(Integer)
    resref      = Column(String)
    recipeId    = Column(String)
    ingredients = Column(String)
    completed   = Column(String)

    @property
    def owned_payload(self):
        return {
            'id'            : self.id,
            'characterId'   : self.characterId,
            'amount'        : self.amount,
            'resref'        : self.resref,
            'recipeId'      : self.recipeId,
            'ingredients'   : self.ingredients,
            'completed'     : self.completed,
        }
