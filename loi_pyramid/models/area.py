# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from .meta import Base


class Area(Base):
    __tablename__ = 'areas'
    
    code = Column(String, primary_key=True, info={'access': 'public'})
    name = Column(String, info={'access': 'public'})
    position = Column(String, info={'access': 'public'})
    movement = Column(Integer, info={'access': 'public'})
