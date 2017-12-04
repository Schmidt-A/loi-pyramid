# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base

class Faction(Base):
    __tablename__ = 'factions'
    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    factionId   = Column(String)
