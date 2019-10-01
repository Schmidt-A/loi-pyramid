# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base


class Recipe(Base):
    __tablename__ = 'recipes'
    
    blueprint = Column(String, primary_key=True, info={'access': 'public'})
    name = Column(String, info={'access': 'public'})
    category = Column(String, info={'access': 'public'})
    actions = Column(Integer, info={'access': 'public'})
    time = Column(Integer, info={'access': 'public'})
    cost = Column(String, info={'access': 'public'})
    building = Column(String, info={'access': 'public'})
