import logging

from ..models import (
    Character, 
    Member, 
    Faction, 
    Reputation, 
    Item, Account, 
    Recipe, 
    Ingredient, 
    Action,
    Area)

# TODO: Fix flask rules for indentation
# TODO: Fix refactor this into a better pattern for handling types of data outputs
#   vs db initialization
# also have a required data pattern for tests 

log = logging.getLogger(__name__)

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
                username='Tweek',
                password='$2b$12$rHfWWZ0quR5x48479dwPBekHeiuhdBtT8A4IQKTC32ifOxhG0FKxK'.encode(
                    'utf8'),
                cdkey='efgh5678',
                role=3,
                approved=1,
                banned=0,
                actions=5),
            #password is dragon4ever
            'aez': Account(
                username='Aez',
                password='$2b$12$rHfWWZ0quR5x48479dwPBekHeiuhdBtT8A4IQKTC32ifOxhG0FKxK'.encode(
                    'utf8'),
                cdkey='asdf1234',
                role=3,
                approved=1,
                banned=0,
                actions=0),
            #password is drizzit4ever
            'noob': Account(
                username='XxDrizzitxX',
                password='$2b$12$QMHEWrZZaw5hhFFhh/92jut4UpQl5nxr8oEYqgppBm3iWFlpS0jJm'.encode(
                    'utf8'),
                cdkey='klmn9911',
                role=1,
                approved=0,
                banned=0)
        }
        self.session.add_all(list(accounts.values()))
        return accounts

    def account_fixture(self):
        accounts = self.account_data()
        test_accounts = self.convert_to_json(accounts)
        return test_accounts

    def fake_account_fixture(self):
        accounts = {
            #password is dicks4ever
            'tam': Account(
                username='TamTamTamTam',
                password='$2b$12$aVzX7hfREVbVNy/UsAIUCu86tw23661kTl8iED8d1TbzreEWp9P0C'.encode(
                    'utf8'),
                cdkey='yzyz8008',
                role=1,
                approved=0,
                banned=0)
        }
        fake_accounts = self.convert_to_json(accounts)
        return fake_accounts

    def character_data(self):
        characters = {
            'siobhan': Character(
                id=1,
                accountId='Tweek',
                name='Siobhan Faulkner',
                exp=10000,
                area='hlammach_docks',
                created='23/11/2017',
                updated='29/11/2017'),
            'alrunden': Character(
                id=2,
                accountId='Aez',
                name='Alrunden Peralt',
                exp=12000,
                area='dreyen_north',
                created='26/6/2017',
                updated='29/11/2017'),
            'arthen': Character(
                id=3,
                accountId=None,
                name='Arthen Relindar',
                exp=20000,
                area='relindar_green',
                created=None,
                updated=None),
            'jilin': Character(
                id=4,
                accountId='XxDrizzitxX',
                name='Ji\'Lin Thri\'quen',
                exp=1050,
                area='dreyen_north',
                created='29/11/2017',
                updated='29/11/2017'),
            'seth': Character(
                id=5,
                accountId='Tweek',
                name='Seth Nottel',
                exp=7000,
                area='dreyen_south',
                created='27/11/2017',
                updated='3/12/2017'),
        }
        self.session.add_all(list(characters.values()))
        return characters

    def fake_character_fixture(self):
        characters = {
            # non existent character, to be used for negative testing
            'meero': Character(
                id=20,
                accountId='Aez',
                name='Meero Isesi',
                exp=2000,
                area='Dreyen Inn',
                created=None,
                updated=None)
        }
        fake_characters = self.convert_to_json(characters)
        return fake_characters

    def item_data(self):
        items = {
            'al_grain': Item(
                id=1,
                characterId=2,
                resref='grain',
                amount=10,
                created=None,
                updated=None),
            'al_cow': Item(
                id=2,
                characterId=2,
                resref='cow',
                amount=5,
                created=None,
                updated=None),
            'al_sheep': Item(
                id=3,
                characterId=2,
                resref='sheep',
                amount=20,
                created=None,
                updated=None),
            'al_money': Item(
                id=4,
                characterId=2,
                resref='gp',
                amount=400,
                created=None,
                updated=None),
            'sio_money': Item(
                id=5,
                characterId=1,
                resref='gp',
                amount=50,
                created=None,
                updated=None),
            'noob_money': Item(
                id=6,
                characterId=4,
                resref='gp',
                amount=11,
                created=None,
                updated=None),
            'noob_copper': Item(
                id=7,
                characterId=4,
                resref='copper',
                amount=3,
                created=None,
                updated=None)
        }
        self.session.add_all(list(items.values()))
        return items

    def fake_item_fixture(self):
        items = {
            # not yet added, to be used for create
            'op_armor': Item(
                id=20,
                characterId=2,
                resref='op_armor',
                amount=1,
                created=None,
                updated=None),
            # non existent item, to be used for negative testing
            'al_zombie': Item(
                id=21,
                characterId=2,
                resref='zombie_guard',
                amount=2,
                created=None,
                updated=None),
            # non existent item, to be used for negative testing
            'cheat_sword': Item(
                id=22,
                characterId=4,
                resref='scimitar_plus_5',
                amount=1,
                created=None,
                updated=None),
        }
        fake_items = self.convert_to_json(items)
        return fake_items

    def recipe_data(self):
        recipes = {
            'exp': Recipe(
                blueprint='exp',
                name='Train Yourself',
                category='exp',
                actions=1,
                time=300,
                cost='',
                building='gym'),
            'longsword': Recipe(
                blueprint='longsword',
                name='Craft {material} Longsword',
                category='melee',
                actions=5,
                time=0,
                cost='metal:10',
                building='smith'),
            'metal': Recipe(
                blueprint='metal',
                name='Mine for {material} Ore',
                category='ingredient',
                actions=1,
                time=0,
                cost='',
                building='mine'),
            'wood': Recipe(
                blueprint='wood',
                name='Chop {material} Wood',
                category='ingredient',
                actions=1,
                time=0,
                cost='',
                building='forest'),
            'city_move': Recipe(
                blueprint='city_move',
                name='Move through city area',
                category='movement',
                actions=1),
            'road_move': Recipe(
                blueprint='road_move',
                name='Move through road area',
                category='movement',
                actions=3),
            'field_move': Recipe(
                blueprint='field_move',
                name='Move through field area',
                category='movement',
                actions=5),
            'forest_move': Recipe(
                blueprint='forest_move',
                name='Move through forest area',
                category='movement',
                actions=8),
            'boat_move': Recipe(
                blueprint='boat_move',
                name='Move through water area',
                category='movement',
                actions=1,
                cost='boat')
        }
        self.session.add_all(list(recipes.values()))
        return recipes

    def fake_recipe_fixture(self):
        recipes = {
            'lyrium': Recipe(
                blueprint='lyrium',
                name='Extract Lyrium',
                category='ingredient',
                actions=10,
                time=1,
                cost='',
                building='mine')
        }
        fake_recipes = self.convert_to_json(recipes)
        return fake_recipes

    def ingredient_data(self):
        ingredients = {
            'iron': Ingredient(
                material='iron',
                name='Iron Ore',
                category='metal',
                tier=0,
                melee_stats='damage:2',
                half_melee_stats='damage:1',
                armor_stats='slash_reduce:2/1',
                half_armor_stats='slash_reduce:2/1'),
            'cold_iron': Ingredient(
                material='cold_iron',
                name='Cold Iron',
                category='metal',
                tier=2,
                melee_stats='damage_demon:2d6',
                half_melee_stats='damage_demon:1d6',
                armor_stats='armor_demon:4',
                half_armor_stats='armor_demon:3'),
            'boat': Ingredient(
                material='boat',
                name='Boat',
                category='travel',
                tier=2)
        }
        self.session.add_all(list(ingredients.values()))
        return ingredients

    def fake_ingredient_fixture(self):
        ingredients = {
            'uranium': Ingredient(
                material='uranium',
                name='Uranium Ore',
                category='metal',
                tier=5,
                melee_stats='enhance:10',
                half_melee_stats='enhance:5',
                armor_stats='armor:10',
                half_armor_stats='armor:5')
        }
        fake_ingredients = self.convert_to_json(ingredients)
        return fake_ingredients

    def action_data(self):
        actions = {
            'al_craft': Action(
                id=1,
                characterId=2,
                amount=1,
                resref='longsword_damage_2',
                blueprint='longsword',
                ingredients='iron:10',
                completed='3000'),
            'noob_train': Action(
                id=2,
                characterId=4,
                amount=5,
                resref='exp_10',
                blueprint='exp',
                ingredients='',
                completed='1500'),
            'noob_mine': Action(
                id=3,
                characterId=4,
                amount=3,
                resref='iron',
                blueprint='iron',
                ingredients='',
                completed='900')
        }
        self.session.add_all(list(actions.values()))
        return actions

    def fake_action_fixture(self):
        actions = {
            'noob_cheat': Action(
                id=14,
                characterId=4,
                amount=2,
                resref='longsword_of_boners',
                blueprint='longsword',
                ingredients='boner:10',
                completed='1'),
        }
        fake_actions = self.convert_to_json(actions)
        return fake_actions

    def faction_data(self):
        factions = {
            'smugglers': Faction(
                id=1,
                name='Smugglers',
                factionId=None),
            'relindars': Faction(
                id=2,
                name='Relindar Family',
                factionId=None),
            'cousins': Faction(
                id=3,
                name='Hlammach Relindar',
                factionId=2)
        }
        self.session.add_all(list(factions.values()))
        return factions

    def member_data(self):
        members = {
            'siobhan_spy': Member(
                id=1,
                characterId=1,
                factionId=1,
                role='member',
                active=1,
                secret=1,
                created='23/11/2017',
                dateLeft=None),
            'al_left': Member(
                id=2,
                characterId=2,
                factionId=1,
                role='member',
                active=0,
                secret=0,
                created='20/7/2017',
                dateLeft='1/10/2017'),
            'al_now': Member(
                characterId=2,
                factionId=3,
                role='member',
                active=1,
                secret=0,
                created='4/11/2017',
                dateLeft=None),
            'arthen_fam': Member(
                id=3,
                characterId=3,
                factionId=3,
                role='family',
                active=1,
                secret=1,
                created=None,
                dateLeft=None)
        }
        self.session.add_all(list(members.values()))
        return members

    def reputation_data(self):
        reputation = {
            'rel_sio': Reputation(
                id=1,
                characterId=None,
                factionId=3,
                amount=-5,
                atCharId=1,
                atFactionId=None),
            'smug_sio': Reputation(
                id=2,
                characterId=None,
                factionId=1,
                amount=80,
                atCharId=1,
                atFactionId=None),
            'rel_al': Reputation(
                id=3,
                characterId=None,
                factionId=3,
                amount=30,
                atCharId=2,
                atFactionId=None),
            'smug_al': Reputation(
                id=4,
                characterId=None,
                factionId=1,
                amount=-30,
                atCharId=2,
                atFactionId=None),
            'rel_arthen': Reputation(
                id=5,
                characterId=None,
                factionId=3,
                amount=90,
                atCharId=3,
                atFactionId=None),
            'arthen_al': Reputation(
                id=6,
                characterId=3,
                factionId=None,
                amount=50,
                atCharId=2,
                atFactionId=None),
            'smug_rel': Reputation(
                id=7,
                characterId=None,
                factionId=1,
                amount=-20,
                atCharId=None,
                atFactionId=2),
            'rel_smug': Reputation(
                id=8,
                characterId=None,
                factionId=2,
                amount=-10,
                atCharId=None,
                atFactionId=1),
            'cou_smug': Reputation(
                id=9,
                characterId=None,
                factionId=3,
                amount=10,
                atCharId=None,
                atFactionId=1)
        }
        self.session.add_all(list(reputation.values()))
        return reputation


    def area_data(self):
        areas = {
            'dreyen_north': Area(
                code='dreyen_north',
                name='Dreyen North',
                position='5,5',
                movement='city_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'dreyen_south': Area(
                code='dreyen_south',
                name='Dreyen South',
                position='4,4',
                movement='road_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'dreyen_runoff': Area(
                code='dreyen_runoff',
                name='Dreyen Runoff',
                position='5,4',
                movement='boat_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'dreyen_fields': Area(
                code='dreyen_fields',
                name='Dreyen Fields',
                position='4,5',
                movement='field_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'orbest_blackharp': Area(
                code='orbest_blackharp',
                name='Dreyen South',
                position='2,3',
                movement='road_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'road_bend': Area(
                code='road_bend',
                name='Dreyen South',
                position='2,4',
                movement='road_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'abbey_fields': Area(
                code='abbey_fields',
                name='Abbey Fields',
                position='1,3',
                movement='road_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'wood_cut': Area(
                code='wood_cut',
                name='Wood Cut',
                position='3,4',
                movement='road_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'hlammach_towers': Area(
                code='hlammach_towers',
                name='Hlammach Towers',
                position='2,0',
                movement='city_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'hlammach_way': Area(
                code='hlammach_way',
                name='Hlammach Way',
                position='2,1',
                movement='road_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'tide_flats': Area(
                code='tide_flats',
                name='Tide Flats',
                position='3,1',
                movement='field_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'hin_town': Area(
                code='hin_town',
                name='Hin Town',
                position='3,2',
                movement='field_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'fish_hook': Area(
                code='fish_hook',
                name='Fish Hook',
                position='3,3',
                movement='field_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'hlammach_docks': Area(
                code='hlammach_docks',
                name='Hlammach Docks',
                position='3,0',
                movement='road_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'hlammach_sound': Area(
                code='hlammach_sound',
                name='Hlammach Sound',
                position='4,0',
                movement='boat_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'hlammach_shoals': Area(
                code='hlammach_shoals',
                name='Hlammach Shoals',
                position='4,1',
                movement='boat_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'wave_right': Area(
                code='wave_right',
                name='Wave Right',
                position='4,2',
                movement='boat_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'flat_shoals': Area(
                code='flat_shoals',
                name='Flat Shoals',
                position='4,1',
                movement='boat_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'hook_shoals': Area(
                code='hook_shoals',
                name='Hook Bend',
                position='4,3',
                movement='boat_move',
                created='1/11/2017',
                updated='1/11/2017'),
            'relindar_green': Area(
                code='relindar_green',
                name='Relindar Green',
                position='3,7',
                movement='boat_move',
                created='1/11/2017',
                updated='1/11/2017')
        }
        self.session.add_all(list(areas.values()))
        return areas

    def fake_area_fixture(self):
        areas = {
            # non existent character, to be used for negative testing
            'sundured_desolation': Area(
                code='sundured_desolation',
                name='Sundured Desolation',
                position='-100,100',
                movement='city_move',
                created='1/11/2017',
                updated='1/11/2017')
        }
        fake_areas = self.convert_to_json(areas)
        return fake_areas
