# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base

# TODO: change updated+created to datetimes. sqlite doesn't support.
class Faction(Base):
    __tablename__ = 'factions'
    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    factionId   = Column(String)
    created     = Column(String)
    updated     = Column(String)
