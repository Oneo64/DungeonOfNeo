import random


class Plot:
    villains = {
        "demon lord": ["demons", "gnolls", "undead"],
        "evil wizard": ["constructs", "elementals", "undead"],
        "vampire": ["undead"],
        "death knight": ["constructs", "undead"],
        "djinni": ["elementals", "kobolds"],
        "mummy lord": ["undead"],
        "nothic": ["undead", "gnolls"],
        "red dragon": ["kobolds", "elementals"],
        "fire giant": ["goblins", "orcs", "kobolds"],
        "minotaur": ["demons", "gnolls"],
        "behir": ["elementals", "kobolds"]
    }

    additional_inhabitants = [
        "blight", "evil orb", "grick"
    ]

    def random(self):
        keys = []

        for k in enumerate(self.villains):
            keys.append(k[1])

        villain = random.choice(keys)

        return [villain]
