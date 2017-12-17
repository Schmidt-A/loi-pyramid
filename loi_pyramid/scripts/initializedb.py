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
from ..models import Character
from ..models import Member
from ..models import Faction
from ..models import Reputation
from ..models import Inventory


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
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        siobhan = Character(
                accountId   = 'Tweek',
                name        = 'Siobhan Faulkner',
                lastLogin   = '29/11/2017',
                created     = '23/11/2017',
                updated     = '29/11/2017')
        alrunden = Character(
                accountId   = 'Aez',
                name        = 'Alrunden Peralt',
                lastLogin   = '29/11/2017',
                created     = '26/6/2017',
                updated     = '29/11/2017')
        arthen = Character(
                accountId   = None,
                name        = 'Arthen Relindar',
                lastLogin   = None,
                created     = None,
                updated     = '29/11/2017')
        dbsession.add_all([siobhan, alrunden, arthen])

        al_grain = Inventory(
                characterId = alrunden.id,
                blueprintId = 'grain',
                amount      = 10,
                created     = None,
                updated     = None)
        al_cow = Inventory(
                characterId = alrunden.id,
                blueprintId = 'cow',
                amount      = 5,
                created     = None,
                updated     = None)
        al_sheep = Inventory(
                characterId = alrunden.id,
                blueprintId = 'sheep',
                amount      = 20,
                created     = None,
                updated     = None)
        al_money = Inventory(
                characterId = alrunden.id,
                blueprintId = 'gp',
                amount      = 400,
                created     = None,
                updated     = None)
        sio_money = Inventory(
                characterId = siobhan.id,
                blueprintId = 'gp',
                amount      = 50,
                created     = None,
                updated     = None)
        dbsession.add_all([sio_money, al_grain, al_cow, al_sheep, al_money])

        smugglers = Faction(
                name        = 'Smugglers',
                factionId   = None)
        relindars = Faction(
                name        = 'Relindar Family',
                factionId   = None)
        cousins = Faction(
                name        = 'Hlammach Relindar',
                factionId   = relindars.id)
        dbsession.add_all([smugglers, relindars, cousins])

        siobhan_spy = Member(
                characterId = siobhan.id,
                factionId   = smugglers.id,
                role        = 'member',
                active      = 1,
                secret      = 1,
                created     = '23/11/2017',
                dateLeft    = None)
        al_left = Member(
                characterId = alrunden.id,
                factionId   = smugglers.id,
                role        = 'member',
                active      = 0,
                secret      = 0,
                created     = '20/7/2017',
                dateLeft    = '1/10/2017')
        al_now = Member(
                characterId = alrunden.id,
                factionId   = cousins.id,
                role        = 'member',
                active      = 1,
                secret      = 0,
                created     = '4/11/2017',
                dateLeft    = None)
        arthen_fam = Member(
                characterId = arthen.id,
                factionId   = cousins.id,
                role        = 'family',
                active      = 1,
                secret      = 1,
                created     = None,
                dateLeft    = None)
        dbsession.add_all([siobhan_spy, al_left, al_now, arthen_fam])

        rel_sio = Reputation(
                characterId = None,
                factionId   = cousins.id,
                amount      = -5,
                atCharId    = siobhan.id,
                atFactionId = None)
        smug_sio = Reputation(
                characterId = None,
                factionId   = smugglers.id,
                amount      = 80,
                atCharId    = siobhan.id,
                atFactionId = None)
        rel_al = Reputation(
                characterId = None,
                factionId   = cousins.id,
                amount      = 30,
                atCharId    = alrunden.id,
                atFactionId = None)
        smug_al = Reputation(
                characterId = None,
                factionId   = smugglers.id,
                amount      = -30,
                atCharId    = alrunden.id,
                atFactionId = None)
        rel_arthen = Reputation(
                characterId = None,
                factionId   = cousins.id,
                amount      = 90,
                atCharId    = arthen.id,
                atFactionId = None)
        arthen_al = Reputation(
                characterId = arthen.id,
                factionId   = None,
                amount      = 50,
                atCharId    = alrunden.id,
                atFactionId = None)
        smug_rel = Reputation(
                characterId = None,
                factionId   = smugglers.id,
                amount      = -20,
                atCharId    = None,
                atFactionId = relindars.id)
        rel_smug = Reputation(
                characterId = None,
                factionId   = relindars.id,
                amount      = -10,
                atCharId    = None,
                atFactionId = smugglers.id)
        cou_smug = Reputation(
                characterId = None,
                factionId   = cousins.id,
                amount      = 10,
                atCharId    = None,
                atFactionId = smugglers.id)
        dbsession.add_all([
                smug_sio,
                smug_rel,
                smug_al,
                cou_smug,
                rel_sio,
                rel_smug,
                rel_arthen,
                rel_al])
