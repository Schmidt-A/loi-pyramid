# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base

# TODO: change updated+created to datetimes. sqlite doesn't support.
class Action(Base):
    __tablename__ = 'actions'
    id          = Column(Integer, primary_key=True)
    characterId = Column(Integer)
    type        = Column(String)
    amount      = Column(Integer)
    recipeId    = Column(Integer)
    completed   = Column(String)
    created     = Column(String)
    updated     = Column(String)
