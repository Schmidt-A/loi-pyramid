from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    accountId   = Column(Integer)
    name        = Column(String)
    factionName = Column(String)
    lastLogin   = Column(String) # TODO: sqlite doesn't support datetime objs, convert later
    created     = Column(String) # Same deal here

    # TODO: move this into base definition
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
