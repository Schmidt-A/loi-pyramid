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
    __table_args__ = {'info':{'access': 'private'}}
    __primary__ = 'actionId'
    
    id = Column(Integer, primary_key=True, info={'access': 'private'})
    characterId = Column(Integer, ForeignKey('characters.id'), info={'access': 'private'})
    amount = Column(Integer, info={'access': 'private'})
    resref = Column(String, info={'access': 'private'})
    blueprint = Column(String, ForeignKey('recipes.blueprint'), info={'access': 'private'})
    # need to redo the ingredients
    ingredients = Column(String, info={'access': 'private'})
    completed = Column(String, info={'access': 'private'})
