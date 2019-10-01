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
    __table_args__ = {'info':{'access': 'private'}}
    __primary__ = 'memberId'

    id = Column(Integer, primary_key=True, info={'access': 'public'})
    characterId = Column(String, ForeignKey('characters.id'), info={'access': 'private'})
    factionId = Column(String, ForeignKey('factions.id'), info={'access': 'private'})
    role = Column(String, info={'access': 'private'})
    active = Column(Integer, info={'access': 'private'})
    secret = Column(Integer, info={'access': 'private'})
    dateLeft = Column(String, info={'access': 'private'})
