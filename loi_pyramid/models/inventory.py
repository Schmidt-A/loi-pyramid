# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base

class Inventory(Base):
    __tablename__ = 'inventory'
    id          = Column(Integer, primary_key=True)
    characterId = Column(Integer)
    blueprintId = Column(Integer)
    amount      = Column(Integer)
    created     = Column(String)
    updated     = Column(String)
