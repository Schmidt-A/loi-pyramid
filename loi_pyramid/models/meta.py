import logging

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.schema import MetaData
from sqlalchemy import Column, String
from datetime import datetime
from sqlalchemy.inspection import inspect

log = logging.getLogger(__name__)

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)

# TOOD: figure out why putting NotImplemented Interface methods causes trouble with hasattr()
@as_declarative(metadata=metadata)
class Base(object):

    created = Column(String)
    updated = Column(String)

    def __json__(self, request):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def set_created(self):
        created = str(datetime.now())

    def set_updated(self):
        updated = str(datetime.now())

    def get_foreign_key_by(self, by_model):
        foreign_keys = list(self.__table__.foreign_keys)
        match_key = inspect(by_model).primary_key[0].key
        for foreign_key in foreign_keys:
            if foreign_key.column.name == match_key:
                log.warning('foreign key found between {} {} and {} {}'.format(
                    self.__tablename__, foreign_key.parent.name,
                    foreign_key.column.table.name, foreign_key.column.name))
                return foreign_key
        