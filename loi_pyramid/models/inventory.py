# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base

# TODO: change updated+created to datetimes. sqlite doesn't support.
class Inventory(Base):
    __tablename__ = 'inventory'
    id          = Column(Integer, primary_key=True)
    characterId = Column(Integer)
    blueprintId = Column(String)
    amount      = Column(Integer)
    created     = Column(String)
    updated     = Column(String)
