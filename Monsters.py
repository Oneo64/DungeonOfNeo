from Skills import DamageType

monsters = {
    # UNDEAD
    "zombie": {
        "health": 22,
        "armor": 8,
        "challenge": 1,
        "weak_to": [DamageType.Radiant],
        "immune_to": [DamageType.Poison, DamageType.Necrotic],
        "stats": {
            "str": 13, "dex": 6, "con": 16, "int": 3, "wis": 6, "chr": 5
        },
        "attacks": ["melee"]
    },
    "darkast": {
        "health": 25,
        "armor": 10,
        "challenge": 2,
        "weak_to": [DamageType.Radiant],
        "immune_to": [DamageType.Poison, DamageType.Necrotic],
        "stats": {
            "str": 14, "dex": 7, "con": 15, "int": 5, "wis": 8, "chr": 6
        },
        "equipment": ["longsword"],
        "attacks": ["melee"]
    },
    "skeleton": {
        "health": 13,
        "armor": 13,
        "challenge": 1,
        "weak_to": [DamageType.Bludgeoning, DamageType.Radiant],
        "immune_to": [DamageType.Poison, DamageType.Necrotic],
        "stats": {
            "str": 10, "dex": 14, "con": 15, "int": 6, "wis": 8, "chr": 5
        },
        "equipment": ["shortsword"],
        "attacks": ["melee"]
    },

    # DEMONS
    "dretch": {
        "health": 18,
        "armor": 11,
        "challenge": 1,
        "weak_to": [DamageType.Radiant],
        "strong_to": [DamageType.Frost, DamageType.Fire, DamageType.Shock],
        "immune_to": [DamageType.Poison],
        "stats": {
            "str": 11, "dex": 11, "con": 12, "int": 5, "wis": 8, "chr": 3
        },
        "equipment": [],
        "attacks": ["claw"]
    },
    "quasit": {
        "health": 7,
        "armor": 13,
        "challenge": 1,
        "weak_to": [DamageType.Radiant],
        "strong_to": [DamageType.Frost, DamageType.Fire, DamageType.Shock],
        "immune_to": [DamageType.Poison],
        "stats": {
            "str": 5, "dex": 17, "con": 10, "int": 7, "wis": 10, "chr": 10
        },
        "equipment": [],
        "attacks": ["claw"]
    },
    "hezrou": {
        "health": 130,
        "armor": 16,
        "challenge": 8,
        "weak_to": [DamageType.Radiant],
        "strong_to": [DamageType.Frost, DamageType.Fire, DamageType.Shock],
        "immune_to": [DamageType.Poison],
        "stats": {
            "str": 19, "dex": 17, "con": 20, "int": 5, "wis": 12, "chr": 13
        },
        "equipment": [],
        "attacks": ["claw"]
    },
    "nalfeshnee": {
        "health": 180,
        "armor": 18,
        "challenge": 13,
        "weak_to": [DamageType.Radiant],
        "strong_to": [DamageType.Frost, DamageType.Fire, DamageType.Shock],
        "immune_to": [DamageType.Poison],
        "stats": {
            "str": 21, "dex": 10, "con": 22, "int": 19, "wis": 12, "chr": 15
        },
        "equipment": [],
        "attacks": ["claw"]
    },
    "balor": {
        "health": 260,
        "armor": 19,
        "challenge": 19,
        "weak_to": [DamageType.Radiant],
        "strong_to": [DamageType.Frost, DamageType.Shock],
        "immune_to": [DamageType.Fire, DamageType.Poison],
        "stats": {
            "str": 26, "dex": 15, "con": 22, "int": 20, "wis": 16, "chr": 22
        },
        "equipment": ["longsword"],
        "attacks": ["melee"]
    }
}

variant_monsters = {
    "skeleton_mage": monsters["skeleton"] | {
        "challenge": 3,
        "attacks": [
            "fire_bolt"
        ],
        "spellcasting_modifier": "int"
    }
}

for i in variant_monsters:
    monsters[i] = variant_monsters[i]

hierarchy = {
    "demon_lord": {
        "high_class": ["balor", "nalfeshnee"],
        "middle_class": ["hezrou", "quasit"],
        "low_class": ["zombie", "skeleton", "darkast", "dretch"]
    }
}
