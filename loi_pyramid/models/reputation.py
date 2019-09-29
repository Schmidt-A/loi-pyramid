# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from .meta import Base


class Reputation(Base):
    __tablename__ = 'reputation'
    __primary__ = 'reputationId'
    id          = Column(Integer, primary_key=True)
    characterId = Column(Integer, ForeignKey('characters.id'))
    factionId   = Column(Integer, ForeignKey('factions.id'))
    amount      = Column(Integer)
    atCharId    = Column(Integer, ForeignKey('characters.id'))
    atFactionId = Column(Integer, ForeignKey('factions.id'))
