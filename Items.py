import json
import random
from enum import Enum

import Utility
from Skills import DamageType


class ItemType(Enum):
    SimpleWeapon = "simple_weapon"
    MartialWeapon = "martial_weapon"
    RangedWeapon = "ranged_weapon"

    Helmet = "helmet"
    Necklace = "necklace"
    Armor = "armor"
    Belt = "belt"
    Boots = "boots"
    Ring = "ring"
    Bracelet = "bracelet"
    Shield = "shield"
    Focus = "focus"


liquids = {
    "water": {
        "health": 1
    },
    "healing_potion": {
        "health": 2,
        "condition": "minor_regeneration"
    },
    "potion_of_regeneration": {
        "condition": "major_regeneration"
    },

    # don't drink these, because it's either bad or it's disgusting
    "poison": {
        "health": -3,
        "condition": "poisoned"
    },
    "blood": {
        "health": -1
    },
    "ink": {
        "health": -1,
        "condition": "poisoned"
    },
    "urine": {
        "condition": "poisoned"
    }
}


items = {
    "junk": {
        "silver_coin": {
            "cost": 1
        },
        "ink_bottle": {
            "weight": 1,
            "cost": 1
        },
        "parchment": {
            "cost": 1
        },
        "map": {
            "cost": 1
        },
        "candle": {
            "cost": 1
        },
        "worn_candle": {
        },
        "ingredient_pouch": {
            "type": ItemType.Focus,
            "cost": 1
        },
        "druidic_orb": {
            "type": ItemType.Focus,
            "cost": 1
        },
        "holy_symbol": {
            "type": ItemType.Focus,
            "cost": 1
        },
        "flask": {
            "can_stack": False,
            "liquid_space": 2,
            "weight": 1,
            "cost": 1
        },
        "bottle": {
            "can_stack": False,
            "liquid_space": 3,
            "weight": 2,
            "cost": 2
        },
        "chalice": {
            "can_stack": False,
            "liquid_space": 3,
            "weight": 5,
            "cost": 2
        },
        "waterskin": {
            "can_stack": False,
            "liquid_space": 4,
            "weight": 4,
            "cost": 1
        },
        "arrow": {
            "weight": 1,
            "cost": 1
        },
        "bolt": {
            "weight": 1,
            "cost": 1
        }
    },
    "consumables": {
        "bread": {
            "on_use": {
                "health": 1,
                "destroy": True
            },
            "weight": 1,
            "cost": 1
        }
    },
    "armors": {
        "gambeson_armor": {
            "type": ItemType.Armor,
            "armor": 1,
            "weight": 5,
            "cost": 5
        },
        "leather_armor": {
            "type": ItemType.Armor,
            "armor": 1,
            "weight": 10,
            "cost": 10
        },
        "studded_leather_armor": {
            "type": ItemType.Armor,
            "armor": 2,
            "weight": 13,
            "cost": 45
        },

        "hide_armor": {
            "type": ItemType.Armor,
            "armor": 2,
            "weight": 12,
            "cost": 10
        },
        "scale_mail_armor": {
            "type": ItemType.Armor,
            "armor": 4,
            "weight": 45,
            "cost": 50
        },
        "breastplate_armor": {
            "type": ItemType.Armor,
            "armor": 5,
            "weight": 20,
            "cost": 400
        },

        "chain_mail_armor": {
            "type": ItemType.Armor,
            "armor": 6,
            "weight": 55,
            "cost": 75
        },
        "splint_armor": {
            "type": ItemType.Armor,
            "armor": 7,
            "weight": 60,
            "cost": 200
        },
        "plate_armor": {
            "type": ItemType.Armor,
            "armor": 8,
            "weight": 65,
            "cost": 1500
        },

        "roundshield": {
            "type": ItemType.Shield,
            "armor": 3,
            "weight": 5,
            "cost": 10
        },
        "kite_shield": {
            "type": ItemType.Shield,
            "armor": 4,
            "weight": 7,
            "cost": 15
        },
        "buckler": {
            "type": ItemType.Shield,
            "armor": 2,
            "weight": 4,
            "cost": 13
        }
    },
    "weapons": {
        "battleaxe": {
            "type": ItemType.MartialWeapon,
            "damage": 4,
            "damage_type": DamageType.Slashing,
            "weight": 4,
            "cost": 10
        },
        "shortsword": {
            "type": ItemType.MartialWeapon,
            "damage": 3,
            "damage_type": DamageType.Piercing,
            "weight": 2,
            "cost": 10
        },
        "arming_sword": {
            "type": ItemType.MartialWeapon,
            "damage": 4,
            "damage_type": DamageType.Slashing,
            "weight": 3,
            "cost": 13
        },
        "longsword": {
            "type": ItemType.MartialWeapon,
            "damage": 5,
            "damage_type": DamageType.Slashing,
            "weight": 4,
            "cost": 15
        },
        "mace": {
            "type": ItemType.SimpleWeapon,
            "damage": 3,
            "damage_type": DamageType.Bludgeoning,
            "weight": 4,
            "cost": 5
        },
        "morningstar": {
            "type": ItemType.MartialWeapon,
            "damage": 4,
            "damage_type": DamageType.Piercing,
            "weight": 4,
            "cost": 15
        },
        "flail": {
            "type": ItemType.MartialWeapon,
            "damage": 4,
            "damage_type": DamageType.Bludgeoning,
            "weight": 2,
            "cost": 10
        },
        "halberd": {
            "type": ItemType.MartialWeapon,
            "damage": 5,
            "damage_type": DamageType.Slashing,
            "weight": 6,
            "cost": 20
        },
        "greatsword": {
            "type": ItemType.MartialWeapon,
            "damage": 8,
            "damage_type": DamageType.Slashing,
            "weight": 6,
            "cost": 50
        },
        "long_axe": {
            "type": ItemType.MartialWeapon,
            "damage": 8,
            "damage_type": DamageType.Slashing,
            "weight": 7,
            "cost": 30
        },
        "scimitar": {
            "type": ItemType.MartialWeapon,
            "damage": 3,
            "damage_type": DamageType.Slashing,
            "weight": 3,
            "cost": 25
        },
        "warhammer": {
            "type": ItemType.MartialWeapon,
            "damage": 4,
            "damage_type": DamageType.Bludgeoning,
            "weight": 2,
            "cost": 15
        },
        "spear": {
            "type": ItemType.SimpleWeapon,
            "damage": 3,
            "damage_type": DamageType.Piercing,
            "weight": 3,
            "cost": 1
        },
        "dagger": {
            "type": ItemType.SimpleWeapon,
            "damage": 2,
            "damage_type": DamageType.Piercing,
            "weight": 1,
            "cost": 2
        },
        "shortbow": {
            "type": ItemType.RangedWeapon,
            "ammunition": "arrow",
            "damage": 3,
            "damage_type": DamageType.Piercing,
            "weight": 2,
            "cost": 25
        },
        "longbow": {
            "type": ItemType.RangedWeapon,
            "ammunition": "arrow",
            "damage": 5,
            "damage_type": DamageType.Piercing,
            "weight": 2,
            "cost": 50
        },
        "crossbow": {
            "type": ItemType.RangedWeapon,
            "ammunition": "bolt",
            "damage": 4,
            "damage_type": DamageType.Piercing,
            "weight": 5,
            "cost": 25
        },
        "heavy_crossbow": {
            "type": ItemType.RangedWeapon,
            "ammunition": "bolt",
            "damage": 6,
            "damage_type": DamageType.Piercing,
            "weight": 18,
            "cost": 50
        },
        "staff": {
            "type": ItemType.SimpleWeapon,
            "damage": 2,
            "damage_type": DamageType.Bludgeoning,
            "weight": 1,
            "cost": 1
        }
    }
}

containers = {
    "storage_chest": {
        "weapons": 0,
        "armor": 0,
        "junk": 1,
        "consumables": 1
    },
    "food_chest": {
        "junk": 1,
        "consumables": 4
    },
    "treasure_chest": {
        "silver": (40, 80),
        "weapons": 0,
        "armor": 0,
        "junk": 2,
        "consumables": 2
    },
    "corpse": {
        "silver": (1, 4),
        "junk": 0,
        "consumables": 0
    },
    "large_stone_goblet": {
        "liquid": [
            "water", "healing_potion", "blood"
        ],
        "liquid_amount": 10
    }
}


def get_item_data(_id):
    for i in items:
        if _id in items[i]:
            return items[i][_id]

    return None


class Item:
    def __init__(self, _id=None):
        if _id is None:
            return

        self.id = _id
        self.amount = 1

        data = get_item_data(_id)

        if "liquid_space" in data:
            self.liquid = ""
            self.liquid_amount = 0

    def get_name(self):
        if hasattr(self, "liquid"):
            data = get_item_data(self.id)

            if self.liquid_amount > 0:
                return Utility.get_name(self.id) + " (" + str(self.liquid_amount) + "/" + str(data["liquid_space"]) + " oz of " + Utility.get_name(self.liquid) + ")"
            else:
                return Utility.get_name(self.id) + " (" + str(data["liquid_space"]) + " FL OZ of space, empty)"

        return Utility.get_name(self.id)

    def fill_with(self, liquid, amount):
        data = get_item_data(self.id)

        if self.liquid_amount >= data["liquid_space"]:
            return[False, "It's already full!"]

        if liquid == self.liquid or self.liquid_amount == 0:
            self.liquid = liquid

            if self.liquid_amount + amount < data["liquid_space"]:
                self.liquid_amount += amount

                return [True, "Added " + str(amount) + " FL OZ of " + Utility.get_name(liquid) + ".", amount]
            else:
                used = data["liquid_space"] - self.liquid_amount
                self.liquid_amount = data["liquid_space"]

                return [True, "Filled with " + Utility.get_name(liquid) + ".", used]
        else:
            return [False, "Cannot fill with liquid, because there is another type of liquid already in it!"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class Container:
    def __init__(self, _id, _items=None, special_name=""):
        if _items is None:
            _items = []

        self.id = _id
        self.items = _items
        self.silver = 0

        if "liquid" in containers[self.id]:
            self.liquid = random.choice(containers[self.id]["liquid"])
            self.liquid_amount = round(random.uniform(0.5, 1) * containers[self.id]["liquid_amount"])

        if special_name != "":
            self.special_name = special_name

    def get_name(self):
        name = Utility.get_name(self.id)

        if hasattr(self, "special_name"):
            name = self.special_name

        if hasattr(self, "liquid"):
            if self.liquid_amount > 0:
                name = Utility.get_name(self.id) + " (" + str(self.liquid_amount) + " FL OZ of " + Utility.get_name(self.liquid) + ")"
            else:
                name = Utility.get_name(self.id) + " (empty)"

        return name

    def create_items(self, level, difficulty):
        multiplier = Utility.multiplier(level, difficulty)
        data = containers[self.id]

        for kvp in enumerate(data):
            value = data[kvp[1]]

            if kvp[1] in items:
                i = value * multiplier

                for i in range(max(i + random.randint(-1, 1), 0)):
                    self.items.append(create_item(kvp[1]))

            if kvp[1] == "silver":
                silver = Item("silver_coin")
                silver.amount = random.randint(value[0], value[1]) * multiplier

                self.items.append(silver)


def create_item(category):
    types = []

    if category == "any":
        types = list(items.keys())
    else:
        types.append(category)

    _items = list(items[random.choice(types)])

    return Item(random.choice(_items))

