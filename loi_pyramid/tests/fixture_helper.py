from ..models import Character
from ..models import Member
from ..models import Faction
from ..models import Reputation
from ..models import Item
from ..models import Account
from ..models import Recipe

#TODO: Fix flask rules for indentation
class FixtureHelper():

    def __init__(self, session):
        self.session = session

    def convert_to_json(self, model_dict):
        test_data = {}
        for key, model in model_dict.items():
            test_data[key] = model.__json__(self)

        return test_data

    def account_data(self):
        accounts = {
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
                username    = 'XxDrizzitxX',
                password    = '$2b$12$QMHEWrZZaw5hhFFhh/92jut4UpQl5nxr8oEYqgppBm3iWFlpS0jJm'.encode('utf8'),
                cdkey       = 'klmn9911',
                role        = 1,
                approved    = 0,
                banned      = 0)
        }
        self.session.add_all(list(accounts.values()))
        test_accounts = self.convert_to_json(accounts)
        return test_accounts

    def fake_account_data(self):
        accounts = {
            #password is dicks4ever
            'tam': Account(
                username    = 'TamTamTamTam',
                password    = '$2b$12$aVzX7hfREVbVNy/UsAIUCu86tw23661kTl8iED8d1TbzreEWp9P0C'.encode('utf8'),
                cdkey       = 'yzyz8008',
                role        = 1,
                approved    = 0,
                banned      = 0)
        }
        fake_accounts = self.convert_to_json(accounts)
        return fake_accounts

    def character_data(self):
        characters = {
            'siobhan': Character(
                id          = 1,
                accountId   = 'Tweek',
                name        = 'Siobhan Faulkner',
                exp         = 10000,
                area        = 'Hlammach Docks',
                created     = '23/11/2017',
                updated     = '29/11/2017'),
            'alrunden': Character(
                id          = 2,
                accountId   = 'Aez',
                name        = 'Alrunden Peralt',
                exp         = 12000,
                area        = 'Dreyen Inn',
                created     = '26/6/2017',
                updated     = '29/11/2017'),
            'arthen': Character(
                id          = 3,
                accountId   = None,
                name        = 'Arthen Relindar',
                exp         = 20000,
                area        = 'Relindar Green',
                created     = None,
                updated     = None),
            'jilin': Character(
                id          = 4,
                accountId   = 'XxDrizzitxX',
                name        = 'Ji\'Lin Thri\'quen',
                exp         = 1050,
                area        = 'Dreyen Inn',
                created     = '29/11/2017',
                updated     = '29/11/2017')
        }
        self.session.add_all(list(characters.values()))
        test_characters = self.convert_to_json(characters)
        return test_characters

    def fake_character_data(self):
        characters = {
            #non existent character, to be used for negative testing
            'meero': Character(
                id          = 20,
                accountId   = 'Aez',
                name        = 'Meero Isesi',
                exp         = 2000,
                area        = 'Dreyen Inn',
                created     = None,
                updated     = None)
        }
        fake_characters = self.convert_to_json(characters)
        return fake_characters

    def item_data(self):
        items = {
            'al_grain': Item(
                id          = 1,
                characterId = 2,
                resref      = 'grain',
                amount      = 10,
                created     = None,
                updated     = None),
            'al_cow': Item(
                id          = 2,
                characterId = 2,
                resref      = 'cow',
                amount      = 5,
                created     = None,
                updated     = None),
            'al_sheep': Item(
                id          = 3,
                characterId = 2,
                resref      = 'sheep',
                amount      = 20,
                created     = None,
                updated     = None),
            'al_money': Item(
                id          = 4,
                characterId = 2,
                resref      = 'gp',
                amount      = 400,
                created     = None,
                updated     = None),
            'sio_money': Item(
                id          = 5,
                characterId = 1,
                resref      = 'gp',
                amount      = 50,
                created     = None,
                updated     = None),
            'noob_money': Item(
                id          = 6,
                characterId = 4,
                resref      = 'gp',
                amount      = 11,
                created     = None,
                updated     = None),
            'noob_copper': Item(
                id          = 7,
                characterId = 4,
                resref      = 'copper',
                amount      = 3,
                created     = None,
                updated     = None)
        }
        self.session.add_all(list(items.values()))
        test_items = self.convert_to_json(items)
        return test_items

    def fake_item_data(self):
        items = {
            #not yet added, to be used for create
            'op_armor': Item(
                id          = 20,
                characterId = 2,
                resref      = 'op_armor',
                amount      = 1,
                created     = None,
                updated     = None),
            #non existent item, to be used for negative testing
            'al_zombie': Item(
                id          = 21,
                characterId = 2,
                resref      = 'zombie_guard',
                amount      = 2,
                created     = None,
                updated     = None),
            #not yet added, to be used for create
            'cheat_sword': Item(
                id          = 22,
                characterId = 4,
                resref      = 'scimitar_plus_5',
                amount      = 1,
                created     = None,
                updated     = None),
        }
        fake_items = self.convert_to_json(items)
        return fake_items

    def recipe_data(self):
        recipes = {
            'exp': Recipe(
                blueprint   = 'exp',
                name        = 'Train Yourself',
                category    = 'exp',
                actions     = 1,
                time        = 300,
                cost        = '',
                requirement = ''),
            'longsword': Recipe(
                blueprint   = 'longsword',
                name        = 'Craft Longsword',
                category    = 'melee',
                actions     = 5,
                time        = 3000,
                cost        = 'metal:10',
                requirement = ''),
            'iron': Recipe(
                blueprint   = 'iron',
                name        = 'Mine for Iron Ore',
                category    = 'metal',
                actions     = 1,
                time        = 300,
                cost        = '',
                requirement = ''),
            'cold_iron': Recipe(
                blueprint   = 'cold_iron',
                name        = 'Mine for Cold Iron',
                category    = 'metal',
                actions     = 3,
                time        = 900,
                cost        = '',
                requirement = 'mining:2')
        }
        self.session.add_all(list(recipes.values()))
        test_recipes = self.convert_to_json(recipes)
        return test_recipes

    def fake_recipe_data(self):
        recipes = {
            'uranium': Recipe(
                blueprint   = 'uranium',
                name        = 'Mine for Uranium',
                category    = 'metal',
                actions     = 10,
                time        = 1,
                cost        = '',
                requirement = '')
        }
        fake_recipes = self.convert_to_json(recipes)
        return fake_recipes

    def faction_data(self):
        factions = {
            'smugglers': Faction(
                id          = 1,
                name        = 'Smugglers',
                factionId   = None),
            'relindars': Faction(
                id          = 2,
                name        = 'Relindar Family',
                factionId   = None),
            'cousins': Faction(
                id          = 3,
                name        = 'Hlammach Relindar',
                factionId   = 2)
        }
        self.session.add_all(list(factions.values()))
        test_factions = self.convert_to_json(factions)
        return test_factions

    def member_data(self):
        members = {
            'siobhan_spy': Member(
                id          = 1,
                characterId = 1,
                factionId   = 1,
                role        = 'member',
                active      = 1,
                secret      = 1,
                created     = '23/11/2017',
                dateLeft    = None),
            'al_left': Member(
                id          = 2,
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
                id          = 3,
                characterId = 3,
                factionId   = 3,
                role        = 'family',
                active      = 1,
                secret      = 1,
                created     = None,
                dateLeft    = None)
        }
        self.session.add_all(list(members.values()))
        test_members = self.convert_to_json(members)
        return test_members

    def reputation_data(self):
        reputation = {
            'rel_sio': Reputation(
                id          = 1,
                characterId = None,
                factionId   = 3,
                amount      = -5,
                atCharId    = 1,
                atFactionId = None),
            'smug_sio': Reputation(
                id          = 2,
                characterId = None,
                factionId   = 1,
                amount      = 80,
                atCharId    = 1,
                atFactionId = None),
            'rel_al': Reputation(
                id          = 3,
                characterId = None,
                factionId   = 3,
                amount      = 30,
                atCharId    = 2,
                atFactionId = None),
            'smug_al': Reputation(
                id          = 4,
                characterId = None,
                factionId   = 1,
                amount      = -30,
                atCharId    = 2,
                atFactionId = None),
            'rel_arthen': Reputation(
                id          = 5,
                characterId = None,
                factionId   = 3,
                amount      = 90,
                atCharId    = 3,
                atFactionId = None),
            'arthen_al': Reputation(
                id          = 6,
                characterId = 3,
                factionId   = None,
                amount      = 50,
                atCharId    = 2,
                atFactionId = None),
            'smug_rel': Reputation(
                id          = 7,
                characterId = None,
                factionId   = 1,
                amount      = -20,
                atCharId    = None,
                atFactionId = 2),
            'rel_smug': Reputation(
                id          = 8,
                characterId = None,
                factionId   = 2,
                amount      = -10,
                atCharId    = None,
                atFactionId = 1),
            'cou_smug': Reputation(
                id          = 9,
                characterId = None,
                factionId   = 3,
                amount      = 10,
                atCharId    = None,
                atFactionId = 1)
        }
        self.session.add_all(list(reputation.values()))
        test_reputation = self.convert_to_json(reputation)
        return test_reputation
