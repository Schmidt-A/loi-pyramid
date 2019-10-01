# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base


class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    material = Column(String, primary_key=True, info={'access': 'public'})
    name = Column(String, info={'access': 'public'})
    category = Column(String, info={'access': 'public'})
    tier = Column(Integer, info={'access': 'public'})
    melee_stats = Column(String, info={'access': 'public'})
    half_melee_stats = Column(String, info={'access': 'public'})
    armor_stats = Column(String, info={'access': 'public'})
    half_armor_stats = Column(String, info={'access': 'public'})
