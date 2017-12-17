# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .meta import Base

# TODO: change updated+created to datetimes. sqlite doesn't support.
# TODO: change ip to CLOB so we can just throw a bunch of ips in there
class Account(Base):
    __tablename__   = 'accounts'
    username    = Column(String, primary_key=True)
    password    = Column(String)
    cdkey       = Column(String)
    ip          = Column(String)
    role        = Column(Integer)
    actions     = Column(Integer)
    approved    = Column(Integer)
    banned      = Column(Integer)
    created     = Column(String)
    updated     = Column(String)
