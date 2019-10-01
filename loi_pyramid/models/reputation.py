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
    __table_args__ = {'info':{'access': 'private'}}
    __primary__ = 'reputationId'

    id = Column(Integer, primary_key=True, info={'access': 'public'})
    characterId = Column(Integer, ForeignKey('characters.id'), info={'access': 'private'})
    factionId = Column(Integer, ForeignKey('factions.id'), info={'access': 'private'})
    amount = Column(Integer, info={'access': 'private'})
    atCharId = Column(Integer, ForeignKey('characters.id'), info={'access': 'private'})
    atFactionId = Column(Integer, ForeignKey('factions.id'), info={'access': 'private'})
