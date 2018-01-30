from ..models import Character
from ..models import Member
from ..models import Faction
from ..models import Reputation
from ..models import Item
from ..models import Account
from ..models import Recipe
from ..models import Ingredient
from ..models import Action

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
            #non existent item, to be used for negative testing
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
                building    = 'gym'),
            'longsword': Recipe(
                blueprint   = 'longsword',
                name        = 'Craft {material} Longsword',
                category    = 'melee',
                actions     = 5,
                time        = 3000,
                cost        = 'metal:10',
                building    = 'smith'),
            'metal': Recipe(
                blueprint   = 'metal',
                name        = 'Mine for {material} Ore',
                category    = 'ingredient',
                actions     = 1,
                time        = 300,
                cost        = '',
                building    = 'mine'),
            'wood': Recipe(
                blueprint   = 'wood',
                name        = 'Chop {material} Wood',
                category    = 'ingredient',
                actions     = 1,
                time        = 300,
                cost        = '',
                building    = 'forest')
        }
        self.session.add_all(list(recipes.values()))
        test_recipes = self.convert_to_json(recipes)
        return test_recipes

    def fake_recipe_data(self):
        recipes = {
            'lyrium': Recipe(
                blueprint   = 'lyrium',
                name        = 'Extract Lyrium',
                category    = 'ingredient',
                actions     = 10,
                time        = 1,
                cost        = '',
                building    = 'mine')
        }
        fake_recipes = self.convert_to_json(recipes)
        return fake_recipes

    def ingredient_data(self):
        ingredients = {
            'iron': Ingredient(
                material            = 'iron',
                name                = 'Iron Ore',
                category            = 'metal',
                tier                = 0,
                melee_stats         = 'damage:2',
                half_melee_stats    = 'damage:1',
                armor_stats         = 'slash_reduce:2/1',
                half_armor_stats    = 'slash_reduce:2/1'),
            'cold_iron': Ingredient(
                material            = 'cold_iron',
                name                = 'Cold Iron',
                category            = 'metal',
                tier                = 2,
                melee_stats         = 'damage_demon:2d6',
                half_melee_stats    = 'damage_demon:1d6',
                armor_stats         = 'armor_demon:4',
                half_armor_stats    = 'armor_demon:3')
        }
        self.session.add_all(list(ingredients.values()))
        test_ingredients = self.convert_to_json(ingredients)
        return test_ingredients

    def fake_ingredient_data(self):
        ingredients = {
            'uranium': Ingredient(
                material            = 'uranium',
                name                = 'Uranium Ore',
                category            = 'metal',
                tier                = 5,
                melee_stats         = 'enhance:10',
                half_melee_stats    = 'enhance:5',
                armor_stats         = 'armor:10',
                half_armor_stats    = 'armor:5')
        }
        fake_ingredients = self.convert_to_json(ingredients)
        return fake_ingredients

    def action_data(self):
        actions = {
            'al_craft': Action(
                id          = 1,
                characterId = 2,
                amount      = 1,
                resref      = 'longsword_damage_2',
                recipeId    = 'longsword',
                ingredients = 'iron:10',
                completed   = '3000'),
            'noob_train': Action(
                id          = 2,
                characterId = 4,
                amount      = 5,
                resref      = 'exp_10',
                recipeId    = 'exp',
                ingredients = '',
                completed   = '1500'),
            'noob_mine': Action(
                id          = 3,
                characterId = 4,
                amount      = 3,
                resref      = 'iron',
                recipeId    = 'iron',
                ingredients = '',
                completed   = '900')
        }
        self.session.add_all(list(actions.values()))
        test_actions = self.convert_to_json(actions)
        return test_actions

    def fake_action_data(self):
        actions = {
            'noob_cheat': Action(
                id          = 14,
                characterId = 4,
                amount      = 2,
                resref      = 'longsword_of_boners',
                recipeId    = 'longsword',
                ingredients = 'boner:10',
                completed   = '1'),
        }
        fake_actions = self.convert_to_json(actions)
        return fake_actions

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
