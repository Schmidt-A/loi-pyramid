# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base

# TODO: change updated+created to datetimes. sqlite doesn't support.
class Reputation(Base):
    __tablename__ = 'reputation'
    id          = Column(Integer, primary_key=True)
    characterId = Column(Integer)
    factionId   = Column(Integer)
    amount      = Column(Integer)
    atCharId    = Column(Integer)
    atFactionId = Column(Integer)
