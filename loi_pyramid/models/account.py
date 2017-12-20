# flake8: noqa
from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    Boolean
)

from .meta import Base

# TODO: change updated+created to datetimes. sqlite doesn't support.
# TODO: Change password to binary because sqlite doesn't support
class Account(Base):
    __tablename__   = 'accounts'
    username    = Column(String, primary_key=True)
    password    = Column(LargeBinary)
    cdkey       = Column(String)
    ip          = Column(String)
    role        = Column(Integer)
    actions     = Column(Integer)
    approved    = Column(Integer)
    banned      = Column(Integer)
    created     = Column(String)
    updated     = Column(String)
