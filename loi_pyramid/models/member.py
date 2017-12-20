# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base

# TODO: change dates to datetimes. sqlite doesn't support.
class Member(Base):
    __tablename__ = 'members'
    id          = Column(Integer, primary_key=True)
    characterId = Column(String)
    factionId   = Column(String)
    role        = Column(String)
    active      = Column(Integer)
    secret      = Column(Integer)
    dateLeft    = Column(String)
    created     = Column(String)
    updated     = Column(String)
