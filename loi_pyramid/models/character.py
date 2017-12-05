# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base

# TODO: change lastLogin+created to datetimes. sqlite doesn't support.
class Character(Base):
    __tablename__ = 'characters'
    id          = Column(Integer, primary_key=True)
    accountId   = Column(Integer)
    name        = Column(String)
    lastLogin   = Column(String)
    created     = Column(String)
