import math
import random
import time

import Creature
import Items
import Monsters
import Utility

room_sizes = {
    "small": 0.5,
    "medium": 1,
    "large": 2,
    "huge": 4
}

# all items here will be multiplied by:
# level + difficulty     result

room_types = {
    "empty_room": {
        "junk": 0,
    },
    "entrance_room": {
    },
    "stair_room": {
    },
    "small_prison": {
        "prisoners": 1,
    },
    "large_prison": {
        "prisoners": 5,
        "junk": 0,
        "possible_rooms": ["corpse_room"]
    },
    "corpse_room": {
        "scene": "A foul smell can be smelled due the amount of rotting bodies here.",
        "junk": 1,
        "monsters": {
            "monsters": ["zombie"],
            "count": 1
        },
        "containers": {
            "corpse": 3
        },
    },
    "research_prison": {
        "scene": "A grotesque mass of flesh lies inside of the cell.",
        "junk": 0,
    },
    "research_room": {
        "weapons": 1,
        "junk": 2,
        "possible_rooms": ["workshop", "research_prison"],
        "containers": {
            "large_stone_goblet": 1
        },
        "monsters": {
            "monsters": ["random_high_class"],
            "count": 1
        }
    },
    "kitchen": {
        "weapons": 0,
        "junk": 3,
        "possible_rooms": ["research_prison", "food_storage_room"],
        "containers": {
            "large_stone_goblet": 2,
            "food_chest": 1
        },
        "monsters": {
            "monsters": ["random_low_class"],
            "count": 4
        }
    },
    "dining_room": {
        "scene": "A long table sits in the middle of the room. Numerous plates and chalices lie on the table, scattered everywhere.",
        "items": {
            "chalice": 3,
            "candle": 1,
            "worn_candle": 2
        },
        "junk": 2,
        "possible_rooms": ["kitchen"],
        "monsters": {
            "monsters": ["random_high_class", "random_middle_class"],
            "count": 3
        }
    },
    "armory": {
        "armors": 2,
        "junk": 0,
        "possible_rooms": ["workshop", "smithy", "research_room"],
        "monsters": {
            "monsters": ["random_middle_class"],
            "count": 1
        }
    },
    "smithy": {
        "weapons": 2,
        "junk": 0,
        "possible_rooms": ["workshop", "armory", "research_room"],
        "monsters": {
            "monsters": ["random_middle_class"],
            "count": 1
        }
    },
    "workshop": {
        "weapons": 1,
        "armors": 1,
        "junk": 3,
        "possible_rooms": ["smithy", "armory", "research_room", "storage_room"],
        "monsters": {
            "monsters": ["random_middle_class", "random_low_class"],
            "count": 3
        }
    },
    "treasure_room": {
        "containers": {
            "treasure_chest": 2
        },
        "silver": (130, 150),
        "weapons": 2,
        "armors": 2,
        "junk": 2,
    },
    "storage_room": {
        "containers": {
            "storage_chest": 4
        },
        "junk": 3,
        "silver": (0, 3),
    },
    "food_storage_room": {
        "containers": {
            "food_chest": 4
        },
        "junk": 1,
    }
}


class Room:
    def __init__(self, room_type):
        self.room_size = "medium"
        self.room_type = room_type

        self.monsters = []
        self.items = []
        self.containers = []
        self.silver = 0

        self.connections = [False, False, False, False]  # north south west east

    def get_desc(self):
        room_name = self.room_type.replace("_", " ")

        if room_name[0] == "a" or room_name[0] == "e" or room_name[0] == "i" or room_name[0] == "o" or room_name[0] == "u":
            desc = "This is an " + room_name + "."
        else:
            desc = "This is a " + room_name + "."

        if "scene" in room_types[self.room_type]:
            desc += " " + room_types[self.room_type]["scene"]

        ways = "\nThere are doors that lead to the:"

        for w in range(len(self.connections)):
            if self.connections[w]:
                if w == 0:
                    ways += " north,"
                if w == 1:
                    ways += " south,"
                if w == 2:
                    ways += " west,"
                if w == 3:
                    ways += " east,"

        desc += ways[:-1] + "."

        silver = 0

        for i in self.items:
            if i.id == "silver_coin":
                silver += i.amount

        if silver > 0:
            desc += "\n"
            if silver >= 500:
                desc += "  A great pile of silver coins lie on the floor!"
            elif silver >= 200:
                desc += "  A pile of silver coins lie on the floor!"
            elif silver >= 100:
                desc += "  There are a lot of silver coins!"
            else:
                desc += "  There are some silver coins."

        if len(self.items) > 0:
            desc += "\n"

            if len(self.items) >= 8:
                desc += "  There are a lot items!"
            elif len(self.items) >= 4:
                desc += "  There are a bunch of items."
            elif len(self.items) > 1:
                desc += "  There are some items."
            else:
                desc += "  There's an item."

        if len(self.containers) > 0:
            containers = {}

            for c in self.containers:
                name = c.get_name()
                containers[name] = (0 if name not in containers else containers[name]) + 1

            desc += "\n  There are "

            for c in containers.keys():
                desc += str(containers[c]) + " " + c + ", "

            desc = desc[:-2] + "."

        return desc

    def create_items(self, level, difficulty):
        multiplier = Utility.multiplier(level, difficulty)
        data = room_types[self.room_type]

        for kvp in enumerate(data):
            value = data[kvp[1]]

            if kvp[1] in Items.items:
                items = value * multiplier

                for i in range(max(items + random.randint(-1, 1), 0)):
                    self.items.append(Items.create_item(kvp[1]))

            if kvp[1] == "items":
                for kvp2 in enumerate(data["items"]):
                    items = data["items"][kvp2[1]] * multiplier

                    for i in range(max(items + random.randint(-1, 1), 0)):
                        self.items.append(Items.Item(kvp2[1]))

            if kvp[1] == "silver":
                silver = Items.Item("silver_coin")
                silver.amount = random.randint(value[0], value[1]) * multiplier

                self.items.append(silver)

            if kvp[1] == "containers":
                for kvp2 in enumerate(data["containers"]):
                    for i in range(data["containers"][kvp2[1]] + random.randint(-1, 1)):
                        container = Items.Container(kvp2[1], [])
                        container.create_items(level, difficulty)

                        self.containers.append(container)

    def create_monsters(self, theme, level, difficulty):
        multiplier = Utility.multiplier(level, difficulty)
        data = room_types[self.room_type]

        if "monsters" in data:
            count = (data["monsters"]["count"] + random.randint(-2, 2)) * multiplier

            for i in range(max(count, 0)):
                _id = random.choice(data["monsters"]["monsters"])

                if _id.startswith("random_"):
                    cls = _id[7:]

                    if cls == "high_class" and random.randint(1, 4) != 1:
                        continue

                    if cls == "medium_class" and random.randint(1, 3) == 1:
                        continue

                    _id = random.choice(Monsters.hierarchy[theme][cls])

                monster = Creature.Creature([_id])

                self.monsters.append(monster)

    def get_next_id(self):
        data = room_types[self.room_type]

        if "possible_rooms" in data:
            if random.randint(1, 2) == 1:
                return random.choice(data["possible_rooms"])

        room = random.choice(list(room_types.keys()))

        while room == "entrance_room" or room == "stair_room":
            room = random.choice(list(room_types.keys()))

        return room
