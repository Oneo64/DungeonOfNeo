from enum import Enum


class DamageType(Enum):
    Slashing = "slashing"
    Piercing = "piercing"
    Bludgeoning = "bludgeoning"

    Magic = "magic"
    Fire = "fire"
    Frost = "frost"
    Shock = "shock"
    Thunder = "thunder"

    Radiant = "radiant"
    Necrotic = "necrotic"

    Acid = "acid"
    Poison = "poison"
    Physic = "physic"


class TargetType(Enum):
    Enemies = "enemy"
    Allies = "Allies"
    Self = "self"


skills = {
    "melee": {
        "damage": 1,
        "damage_type": DamageType.Slashing,
        "range": "melee"
    },
    "claw": {
        "damage": 4,
        "damage_type": DamageType.Slashing,
        "range": "melee"
    },
    "slam": {
        "damage": 7,
        "damage_type": DamageType.Bludgeoning,
        "range": "melee"
    },
    "fire_bolt": {
        "damage": 5,
        "damage_type": DamageType.Fire
    },
    "magic_missile": {
        "damage": 10,
        "cost": 1,
        "area": 1,
        "damage_type": DamageType.Magic
    },
    "fireball": {
        "damage": 30,
        "cost": 3,
        "area": 2,
        "damage_type": DamageType.Fire
    },
    "lightning_bolt": {
        "damage": 40,
        "cost": 3,
        "damage_type": DamageType.Shock
    },
    "eldritch_blast": {
        "damage": 5,
        "damage_type": DamageType.Shock
    },
    "enthrall": {
        "condition": "enthralled",
        "cost": 1
    },
    "fear": {
        "condition": "frightened",
        "cost": 2
    },
    "curse_of_undeath": {
        "condition": "curse_of_undeath",
        "cost": 4
    },
    "mage_armor": {
        "condition": "mage_armor",
        "cost": 1,
        "target": TargetType.Allies
    },
    "invisibility": {
        "condition": "invisibility",
        "cost": 2,
        "target": TargetType.Self
    },
    "hold_person": {
        "condition": "paralyzed",
        "cost": 2
    },
    "magic_weapon": {
        "condition": "magic_weapon",
        "cost": 2
    },
    "remove_curse": {
        "removes_curses": 0,
        "cost": 3
    },
    "blight": {
        "condition": "blighted",
        "cost": 4
    },
    "wall_of_fire": {
        "object": "wall_of_fire",
        "cost": 4
    }
}

conditions = {
    "poisoned": {
        "health": -1,
        "con": -1,
        "duration": 20,
    },
    "minor_regeneration": {
        "health": 1,
        "duration": 5,
    },
    "major_regeneration": {
        "health": 5,
        "duration": 5,
    },
    "mage_armor": {
        "armor": 5,
        "duration": 10,
    }
}