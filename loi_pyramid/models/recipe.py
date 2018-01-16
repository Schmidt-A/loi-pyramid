# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base


class Recipe(Base):
    __tablename__ = 'recipes'
    blueprint   = Column(String, primary_key=True)
    name        = Column(String)
    category    = Column(String)
    actions     = Column(Integer)
    time        = Column(Integer)
    cost        = Column(String)
    requirement = Column(String)

    @property
    def public_payload(self):
        return {
            'blueprint'     : self.blueprint,
            'name'          : self.name,
            'category'      : self.category,
            'actions'       : self.actions,
            'time'          : self.time,
            'cost'          : self.cost,
            'requirement'   : self.requirement
        }
