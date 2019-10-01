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

# TOOD: figure out why putting NotImplemented Interface methods causes
# trouble with hasattr()
@as_declarative(metadata=metadata)
class Base(object):
    __table_args__ = {'info':{'access': 'public'}}

    created = Column(String, default=str(datetime.now()), info={'access': 'public'})
    updated = Column(String, default=str(datetime.now()), info={'access': 'public'})

    #this still exists because we don't want to include secret columns (pw) in the others
    def __json__(self, request):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get_foreign_key_by(self, by_model):
        foreign_keys = list(self.__table__.foreign_keys)
        match_key = inspect(by_model).primary_key[0].key
        for foreign_key in foreign_keys:
            if foreign_key.column.name == match_key:
                log.warning('foreign key found between {} {} and {} {}'.format(
                    self.__tablename__, foreign_key.parent.name,
                    foreign_key.column.table.name, foreign_key.column.name))
                return foreign_key

    def get_by_access(self, access):
        return filter(lambda c: c.info['access'] == access, self.__table__.columns)

    def __private__(self):
        return list(map(lambda c: c.name, self.get_by_access(self, 'private')))

    def __public__(self):
        if self.__table__.info['access'] == 'public':
            return list(map(lambda c: c.name, self.get_by_access(self, 'public')))
        else:
            return []

    def __owned__(self):
        return self.__public__(self) + self.__private__(self)

    @property
    def owned_payload(self):
        return {c.name: getattr(self, c.name) 
            for c in list(self.get_by_access('private')) + list(self.get_by_access('public'))}

    @property
    def public_payload(self):
        if self.__table__.info['access'] == 'public':
            return {c.name: getattr(self, c.name) 
                for c in list(self.get_by_access('public'))}
        else:
            return None
