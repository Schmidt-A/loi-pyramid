from ..models import Character
from ..models import Member
from ..models import Faction
from ..models import Reputation
from ..models import Inventory
from ..models import Account

#TODO: Fix flask rules for indentation
class FixtureHelper():
    def account_data(self):
        return {
            #password is dragon4ever
            'tweek': Account(
                username    = 'Tweek',
                password    = '$2b$12$rHfWWZ0quR5x48479dwPBekHeiuhdBtT8A4IQKTC32ifOxhG0FKxK'.encode('utf8'),
                cdkey       = 'efgh5678',
                role        = 3,
                approved    = 1,
                banned      = 0),
            #password is dragon4ever
            'aez': Account(
                username    = 'Aez',
                password    = '$2b$12$rHfWWZ0quR5x48479dwPBekHeiuhdBtT8A4IQKTC32ifOxhG0FKxK'.encode('utf8'),
                cdkey       = 'asdf1234',
                role        = 3,
                approved    = 1,
                banned      = 0),
            #password is drizzit4ever
            'noob': Account(
                username    = 'XxDrizztxX',
                password    = '$2b$12$QMHEWrZZaw5hhFFhh/92jut4UpQl5nxr8oEYqgppBm3iWFlpS0jJm'.encode('utf8'),
                cdkey       = 'klmn9911',
                role        = 1,
                approved    = 0,
                banned      = 0)
        }

    def fake_account_data(self):
        return {
            #password is dicks4ever
            'tam': Account(
                username    = 'TamTamTamTam',
                password    = '$2b$12$aVzX7hfREVbVNy/UsAIUCu86tw23661kTl8iED8d1TbzreEWp9P0C'.encode('utf8'),
                cdkey       = 'yzyz8008',
                role        = 1,
                approved    = 0,
                banned      = 0)
        }

    def character_data(self):
        return {
            'siobhan': Character(
                accountId   = 'Tweek',
                name        = 'Siobhan Faulkner',
                exp         = 10000,
                area        = 'Hlammach Docks',
                created     = '23/11/2017',
                updated     = '29/11/2017'),
            'alrunden': Character(
                accountId   = 'Aez',
                name        = 'Alrunden Peralt',
                exp         = 12000,
                area        = 'Dreyen Inn',
                created     = '26/6/2017',
                updated     = '29/11/2017'),
            'arthen': Character(
                accountId   = None,
                name        = 'Arthen Relindar',
                exp         = 20000,
                area        = 'Relindar Green',
                created     = None,
                updated     = None),
            'jilin': Character(
                accountId   = 'XxDrizztxX',
                name        = 'Ji\'Lin Thri\'quen',
                exp         = 1050,
                area        = 'Dreyen Inn',
                created     = '29/11/2017',
                updated     = '29/11/2017')
        }

    def fake_character_data(self):
        return {
            #non existent character, to be used for negative testing
            'meero': Character(
                id          = 20,
                accountId   = 2,
                name        = 'Meero Isesi',
                created     = None,
                updated     = None)
        }

    def inventory_data(self):
        return {
            'al_grain': Inventory(
                characterId = 2,
                blueprintId = 'grain',
                amount      = 10,
                created     = None,
                updated     = None),
            'al_cow': Inventory(
                characterId = 2,
                blueprintId = 'cow',
                amount      = 5,
                created     = None,
                updated     = None),
            'al_sheep': Inventory(
                characterId = 2,
                blueprintId = 'sheep',
                amount      = 20,
                created     = None,
                updated     = None),
            'al_money': Inventory(
                characterId = 2,
                blueprintId = 'gp',
                amount      = 400,
                created     = None,
                updated     = None),
            'sio_money': Inventory(
                characterId = 1,
                blueprintId = 'gp',
                amount      = 50,
                created     = None,
                updated     = None),
            'noob_money': Inventory(
                characterId = 4,
                blueprintId = 'gp',
                amount      = 11,
                created     = None,
                updated     = None)
        }

    def fake_inventory_data(self):
        return {
            #not yet added, to be used for create
            'op_armor': Inventory(
                characterId = 2,
                blueprintId = 'op_armor',
                amount      = 1,
                created     = None,
                updated     = None),
            #non existent item, to be used for negative testing
            'al_zombie': Inventory(
                characterId = 2,
                blueprintId = 'zombie_guard',
                amount      = 2,
                created     = None,
                updated     = None)
        }

    def faction_data(self):
        return {
            'smugglers': Faction(
                name        = 'Smugglers',
                factionId   = None),
            'relindars': Faction(
                name        = 'Relindar Family',
                factionId   = None),
            'cousins': Faction(
                name        = 'Hlammach Relindar',
                factionId   = 2)
        }

    def member_data(self):
        return {
            'siobhan_spy': Member(
                characterId = 1,
                factionId   = 1,
                role        = 'member',
                active      = 1,
                secret      = 1,
                created     = '23/11/2017',
                dateLeft    = None),
            'al_left': Member(
                characterId = 2,
                factionId   = 1,
                role        = 'member',
                active      = 0,
                secret      = 0,
                created     = '20/7/2017',
                dateLeft    = '1/10/2017'),
            'al_now': Member(
                characterId = 2,
                factionId   = 3,
                role        = 'member',
                active      = 1,
                secret      = 0,
                created     = '4/11/2017',
                dateLeft    = None),
            'arthen_fam': Member(
                characterId = 3,
                factionId   = 3,
                role        = 'family',
                active      = 1,
                secret      = 1,
                created     = None,
                dateLeft    = None)
        }

    def reputation_data(self):
        return {
            'rel_sio': Reputation(
                characterId = None,
                factionId   = 3,
                amount      = -5,
                atCharId    = 1,
                atFactionId = None),
            'smug_sio': Reputation(
                characterId = None,
                factionId   = 1,
                amount      = 80,
                atCharId    = 1,
                atFactionId = None),
            'rel_al': Reputation(
                characterId = None,
                factionId   = 3,
                amount      = 30,
                atCharId    = 2,
                atFactionId = None),
            'smug_al': Reputation(
                characterId = None,
                factionId   = 1,
                amount      = -30,
                atCharId    = 2,
                atFactionId = None),
            'rel_arthen': Reputation(
                characterId = None,
                factionId   = 3,
                amount      = 90,
                atCharId    = 3,
                atFactionId = None),
            'arthen_al': Reputation(
                characterId = 3,
                factionId   = None,
                amount      = 50,
                atCharId    = 2,
                atFactionId = None),
            'smug_rel': Reputation(
                characterId = None,
                factionId   = 1,
                amount      = -20,
                atCharId    = None,
                atFactionId = 2),
            'rel_smug': Reputation(
                characterId = None,
                factionId   = 2,
                amount      = -10,
                atCharId    = None,
                atFactionId = 1),
            'cou_smug': Reputation(
                characterId = None,
                factionId   = 3,
                amount      = 10,
                atCharId    = None,
                atFactionId = 1)
        }
