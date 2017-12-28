import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..tests.fixture_helper import FixtureHelper

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)

    #dropping all tables then creating all of them for a migration for fixture test data
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        characters = FixtureHelper.character_data(dbsession)
        for name, character in characters.items():
            dbsession.add(character)

        accounts = FixtureHelper.account_data(dbsession)
        for name, account in accounts.items():
            dbsession.add(account)

        items = FixtureHelper.items_data(dbsession)
        for name, item in items.items():
            dbsession.add(item)

        factions = FixtureHelper.faction_data(dbsession)
        for name, faction in factions.items():
            dbsession.add(faction)

        members = FixtureHelper.member_data(dbsession)
        for name, member in members.items():
            dbsession.add(member)

        reputations = FixtureHelper.reputation_data(dbsession)
        for name, reputation in reputations.items():
            dbsession.add(reputation)
