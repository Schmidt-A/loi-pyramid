# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from .meta import Base


class Member(Base):
    __tablename__ = 'members'
    __primary__ = 'memberId'
    id          = Column(Integer, primary_key=True)
    characterId = Column(String, ForeignKey('characters.id'))
    factionId   = Column(String, ForeignKey('factions.id'))
    role        = Column(String)
    active      = Column(Integer)
    secret      = Column(Integer)
    dateLeft    = Column(String)
