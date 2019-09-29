# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from .meta import Base


class Action(Base):
    __tablename__ = 'actions'
    __primary__ = 'actionId'
    id          = Column(Integer, primary_key=True)
    characterId = Column(Integer, ForeignKey('characters.id'))
    amount      = Column(Integer)
    resref      = Column(String)
    blueprint   = Column(String, ForeignKey('recipes.blueprint'))
    #need to redo the ingredients
    ingredients = Column(String)
    completed   = Column(String)

    @property
    def owned_payload(self):
        return {
            'id'            : self.id,
            'characterId'   : self.characterId,
            'amount'        : self.amount,
            'resref'        : self.resref,
            'blueprint'      : self.blueprint,
            'ingredients'   : self.ingredients,
            'completed'     : self.completed,
        }
