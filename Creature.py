import json
import math
import random

import Items
import Skills
import Utility
import Monsters
from Skills import DamageType

races = {
    "dwarf": {
        "stats": {"str": 2, "con": 1}
    },
    "elf": {
        "stats": {"dex": 2, "int": 1}
    },
    "human": {
        "stats": {"int": 1, "chr": 2}
    },
    "gnome": {
        "stats": {"str": -1, "con": -1, "int": 2, "chr": 2}
    }
}

player_classes = {
    "druid": {
        "health": 6,
        "proficiencies": ["hide_armor", "leather_armor", "gambeson_armor", "studded_leather_armor", "shield", "simple_weapon", "druidic_orb"],
        "equipment": ["hide_armor", "parchment", "ink_bottle", "druidic_orb"],
        "spellcasting_modifier": "wis",
        "spell_slots": 4,
    },
    "fighter": {
        "health": 12,
        "proficiencies": ["simple_weapon", "martial_weapon", "shield", "armor"],
        "equipment": ["arming_sword", "roundshield", "gambeson_armor"],
        "spellcasting_modifier": "int",
        "spell_slots": 1,
    },
    "ranger": {
        "health": 8,
        "proficiencies": ["ranged_weapon", "simple_weapon", "hide_armor", "leather_armor", "gambeson_armor", "studded_leather_armor"],
        "equipment": ["shortbow", "dagger"] + (["arrow"] * 20),
        "spellcasting_modifier": "wis",
        "spell_slots": 1,
    },
    "rogue": {
        "health": 10,
        "proficiencies": ["simple_weapon", "crossbow", "hide_armor", "leather_armor", "gambeson_armor", "studded_leather_armor"],
        "equipment": ["dagger", "leather_armor"],
        "spellcasting_modifier": "int",
        "spell_slots": 1,
    },
    "paladin": {
        "health": 10,
        "proficiencies": ["martial_weapon", "armor", "holy_symbol"],
        "equipment": ["arming_sword", "roundshield", "chain_mail_armor", "holy_symbol"],
        "spells": [
            [],
            [],
            []
        ],
        "spellcasting_modifier": "chr",
        "spell_slots": 2,
    },
    "warlock": {
        "health": 6,
        "proficiencies": ["simple_weapon", "gambeson_armor", "leather_armor", "studded_leather_armor", "crossbow", "ingredient_pouch"],
        "equipment": ["parchment", "ink_bottle", "ingredient_pouch", "crossbow", "dagger", "leather_armor"] + (["bolt"] * 20),
        "spells": [
            ["eldritch_blast"],
            ["invisibility", "enthrall"],
            ["fear", "remove_curse", "hold_person"],
            ["curse_of_undeath", "blight"]
        ],
        "spellcasting_modifier": "chr",
        "spell_slots": 4,
    },
    "wizard": {
        "health": 6,
        "proficiencies": ["staff", "dagger", "crossbow", "ingredient_pouch"],
        "equipment": ["ink_bottle", "bottle", "ingredient_pouch", "dagger"] + (["parchment"] * 10),
        "spells": [
            ["fire_bolt", "magic_missile", "mage_armor"],
            ["invisibility", "magic_weapon", "hold_person"],
            ["fireball", "lightning_bolt", "remove_curse"],
            ["blight", "conjure_minor_elementals", "wall_of_fire"]
        ],
        "spellcasting_modifier": "int",
        "spell_slots": 5,
    },
    "all": {
        "equipment": ["bread", "waterskin"]
    }
}


class Creature:
    def __init__(self, data=None):
        if data is None:
            return

        self.equipment = []
        self.stats = {
            "str": random.randint(6, 16),
            "dex": random.randint(6, 16),
            "con": random.randint(6, 16),
            "int": random.randint(6, 16),
            "wis": random.randint(6, 16),
            "chr": random.randint(6, 16)
        }

        self.pos = 0

        self.conditions = []

        if len(data) == 3:
            self.id = "player"
            self.name = data[0]
            self.race = data[1]
            self.player_class = data[2]

            self.level = 1
            self.experience = 0
            self.inventory = []
            self.spells = []

            self.spell_slots = self.get_spell_slots()

            for stat in races[self.race]["stats"]:
                self.stats[stat] += races[self.race]["stats"][stat]

            for i in player_classes[self.player_class]["equipment"] + player_classes["all"]["equipment"]:
                item = Items.Item(i)
                hit = False

                data = Items.get_item_data(i)

                if ("can_stack" not in data or data["can_stack"]) and "type" not in data:
                    for i2 in self.inventory:
                        if i2.id == i:
                            i2.amount += 1
                            hit = True
                            break

                if not hit:
                    self.inventory.append(item)

            self.inventory = sorted(self.inventory, key=lambda x: x.id)
            self.stomach_size = 10
        else:
            self.id = data[0]
            self.stats = Monsters.monsters[data[0]]["stats"]

            if "equipment" in Monsters.monsters[data[0]]:
                for i in Monsters.monsters[data[0]]["equipment"]:
                    item = Items.Item(i)
                    hit = False

                    data = Items.get_item_data(i)

                    if ("can_stack" not in data or data["can_stack"]) and "type" not in data:
                        for i2 in self.equipment:
                            if i2.id == i:
                                i2.amount += 1
                                hit = True
                                break

                    if not hit:
                        self.equipment.append(item)

        self.health = self.get_health()
        self.equipment = sorted(self.equipment, key=lambda x: x.id)

    def give(self, item):
        data = Items.get_item_data(item.id)

        if ("can_stack" not in data or data["can_stack"]) and "type" not in data:
            for i in self.inventory:
                if i.id == item.id:
                    i.amount += item.amount
                    return

        self.inventory.append(item)
        self.inventory = sorted(self.inventory, key=lambda x: x.id)

    def has_item(self, item):
        for i in self.inventory:
            if i.id == item and i.amount > 0:
                return True

        return False

    def remove_item(self, item, amount=1):
        for i in self.inventory:
            if i.id == item:
                i.amount -= amount

                if i.amount <= 0:
                    self.inventory.remove(i)
                    self.inventory = sorted(self.inventory, key=lambda x: x.id)

                return

    def add_condition(self, _id):
        data = Skills.conditions[_id]

        for i in self.conditions:
            if i[0] == _id:
                i[1] = data["duration"]
                return

        self.conditions.append([_id, data["duration"]])

    def use_item(self, item):
        data = Items.get_item_data(item.id)

        if "on_use" in data:
            if "health" in data["on_use"]:
                self.health += data["on_use"]["health"]

            if data["on_use"]["destroy"]:
                item.amount -= 1

                if item.amount <= 0:
                    self.inventory.remove(item)
                    self.inventory = sorted(self.inventory, key=lambda x: x.id)

            self.health = min(self.health, self.get_health())

            return [True, "You used " + item.get_name() + "."]

        if hasattr(item, "liquid"):
            msg = "It's empty."

            if item.liquid_amount > 0:
                liquid = Items.liquids[item.liquid]

                msg = "You drank some " + item.liquid + "."

                if item.liquid == "blood":
                    msg = "You drank some blood. That's disgusting."

                if "health" in liquid:
                    self.health += liquid["health"]

                if "condition" in liquid:
                    self.add_condition(liquid["condition"])

                item.liquid_amount -= 1

                if item.liquid_amount <= 0:
                    item.liquid = ""

                self.health = min(self.health, self.get_health())

            return [True, msg]

        if "type" in data:
            if item in self.inventory:
                prof0 = data["type"].value
                prof1 = item.id

                proficiencies = player_classes[self.player_class]["proficiencies"]

                if prof0 in proficiencies or prof1 in proficiencies:
                    # remove existing equipment, so players cant gain benefits from more than one armor/weapon
                    for i in self.equipment:
                        t0 = Items.get_item_data(i.id)["type"]
                        t1 = data["type"]

                        if t0 == t1 or ("weapon" in t0.value and "weapon" in t1.value):
                            self.inventory.append(i)
                            self.equipment.remove(i)

                    self.equipment.append(item)
                    self.inventory.remove(item)
            else:
                self.inventory.append(item)
                self.equipment.remove(item)

            self.equipment = sorted(self.equipment, key=lambda x: x.id)

            return [False, ""]

        return [False, "You can't use that."]

    def get_carry_weight(self):
        return self.stats["str"] * 5

    def get_carrying_weight(self):
        weight = 0

        for i in self.inventory + self.equipment:
            data = Items.get_item_data(i.id)

            if "weight" in data:
                weight += data["weight"] * i.amount

        return weight

    def get_stat(self, stat):
        s = self.stats[stat]

        if hasattr(self, "player_class") and self.get_carrying_weight() > self.get_carry_weight():
            if stat == "chr":
                s -= 1

            if stat == "dex":
                s -= 3

            if stat == "str":
                s -= 2

        for i in self.conditions:
            data = Skills.conditions[i[0]]

            for k in list(data.keys()):
                if k == stat:
                    s += data[k]

        return max(s, 1)

    def get_stat_modifier(self, stat):
        if stat == "spellcasting":
            if hasattr(self, "player_class"):
                return math.floor((self.get_stat(player_classes[self.player_class]["spellcasting_modifier"]) - 10) / 2)
            else:
                return math.floor((self.stats[Monsters.monsters[self.id]["spellcasting_modifier"]] - 10) / 2)

        return math.floor((self.get_stat(stat) - 10) / 2)

    def damage(self, damage, damage_type):
        dmg = damage
        weak = False

        if not hasattr(self, "player_class"):
            data = Monsters.monsters[self.id]

            if "immune_to" in data and damage_type in data["immune_to"]:
                return 0

            if "strong_to" in data and damage_type in data["strong_to"]:
                dmg = round(dmg / 2)

            if "weak_to" in data and damage_type in data["weak_to"]:
                dmg *= 2
                weak = True

        if random.randint(1, 20) >= self.get_armor() and not weak:
            dmg = round(dmg / 2)

        self.health -= dmg

        return dmg

    def get_weapon_data(self):
        for i in self.equipment:
            data = Items.get_item_data(i.id)

            if "type" in data:
                if "weapon" in data["type"].value:
                    return [i.id, data["damage"], data["damage_type"], data["type"]]

        return ["fists", 1, DamageType.Bludgeoning, Items.ItemType.SimpleWeapon]

    def get_armor(self):
        if self.id in Monsters.monsters:
            if "armor" in Monsters.monsters[self.id]:
                return Monsters.monsters[self.id]["armor"]

        armor = 10

        for i in self.equipment:
            data = Items.get_item_data(i.id)

            if "armor" in data:
                armor += data["armor"]

        return armor

    def print_character(self):
        print("~~~~~~~[" + self.name + "]~~~~~~~")
        print("  Race:       " + self.race)
        print("  Class:      " + self.player_class)
        print()

        def get_stat_str(stat):
            _str = str(self.stats[stat])

            return (" " if len(_str) == 1 else "") + _str

        print("  Str " + get_stat_str("str") + " | Dex " + get_stat_str("dex") + " | Con " + get_stat_str("con"))
        print("  Int " + get_stat_str("int") + " | Wis " + get_stat_str("wis") + " | Chr " + get_stat_str("chr"))
        print()
        print("  Health:     " + str(self.health) + "/" + str(self.get_health()))
        print("  Level       " + str(self.level))
        print("  Experience: " + str(self.experience) + "/" + str(self.get_experience()))

        l = ""

        if hasattr(self, "player_class") and self.get_carrying_weight() > self.get_carry_weight():
            l = "Encumbered, "

        if len(self.conditions) > 0:
            for i in self.conditions:
                l += Utility.get_name(i[0]) + " (" + str(i[1]) + "), "

        if l == "":
            l = "No conditions."
        else:
            l = l[:-2]

        print("  Conditions: " + l)

    def get_health(self):
        if self.id in Monsters.monsters:
            return Monsters.monsters[self.id]["health"]
        else:
            return math.floor(player_classes[self.player_class]["health"] * (0.5 + (self.level * 0.5))) + self.get_stat_modifier("con")

    def get_spell_slots(self):
        data = player_classes[self.player_class]

        return math.floor(data["spell_slots"] * (0.5 + (self.level * 0.5))) + self.get_stat_modifier("int")

    def get_experience(self):
        if hasattr(self, "level"):
            return pow(self.level + 1, 4) * 2
        else:
            return math.ceil(pow(Monsters.monsters[self.id]["challenge"] + 1, 4) * 1.5)

    def get_name(self):
        if hasattr(self, "name"):
            return self.name
        else:
            return Utility.get_name(self.id)

    def get_spells(self):
        spells = []

        if "spells" in player_classes[self.player_class]:
            for level in enumerate(player_classes[self.player_class]["spells"]):
                if math.floor(self.level / 2) >= level[0]:
                    spells += level[1]

        return sorted(spells)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


def save_character(char):
    data = json.dumps(char, cls=JSONEncoder)
    file = open("saves/" + char.name + ".json", "w")

    file.write(data)


def load_character(char):
    with open("saves/" + char, "r") as dat:
        data = json.load(dat)

    character = Creature()

    for key in data.keys():
        if key != "inventory" or key != "equipment":
            character.__setattr__(key, data[key])

    character.inventory = []
    character.equipment = []

    for i in data["inventory"]:
        item = Items.Item()

        for key2 in i:
            item.__setattr__(key2, i[key2])

        character.inventory.append(item)

    for i in data["equipment"]:
        item = Items.Item()

        for key2 in i:
            item.__setattr__(key2, i[key2])

        character.equipment.append(item)

    return character

