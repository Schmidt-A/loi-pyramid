# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base

class Recipe(Base):
    __tablename__ = 'recipe'
    id          = Column(Integer, primary_key=True)
    blueprintId = Column(Integer)
    actions     = Column(Integer)
    time        = Column(Integer)
    cost        = Column(String)
    requirement = Column(String)
    created     = Column(String)
    updated     = Column(String)
