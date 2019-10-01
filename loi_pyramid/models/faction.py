# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from .meta import Base


class Faction(Base):
    __tablename__ = 'factions'
    __primary__ = 'factionId'
    
    id = Column(Integer, primary_key=True, info={'access': 'public'})
    name = Column(String, info={'access': 'public'})
    factionId = Column(String, info={'access': 'public'})
