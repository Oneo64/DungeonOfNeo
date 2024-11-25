import math
import random
import time

import Creature
import Getch
import Items
import Monsters
import Rooms
import Skills
import Utility


class Game:
    def __init__(self, theme, players, difficulty):
        self.theme = theme
        self.players = players
        self.px_old = 10
        self.py_old = 10
        self.px = 10
        self.py = 10

        self.difficulty = difficulty
        self.difficulty_multiplier = [0.5, 1, 1.5][difficulty]

        self.map = []
        self.map2 = []

        for y in range(21):
            self.map.append([False] * 21)
            self.map2.append([False] * 21)

        self.level = 1
        self.set_room(10, 10, "entrance_room")
        self.spread_rooms(4 + difficulty + self.level)

    def load_level(self, level):
        self.px = 10
        self.py = 10

        self.map = []
        self.map2 = []

        for y in range(21):
            self.map.append([False] * 21)
            self.map2.append([False] * 21)

        self.level = level
        self.set_room(10, 10, "entrance_room")
        self.spread_rooms(4 + self.difficulty + self.level)

    def set_stairs(self):
        available = []

        for y in range(21):
            for x in range(21):
                room = self.get_room(x, y)

                if room:
                    dist = math.dist((0, 0), (0, 0))

                    if dist >= 3 + self.difficulty + self.level:
                        available.append((x, y))

        pos = random.choice(available)

        self.set_room(pos[0], pos[1], "stair_room")

    def game_loop(self):
        message = ""

        while True:
            for p in self.players:
                Creature.save_character(p)

            Utility.clear()
            room = self.get_room(self.px, self.py)

            if len(room.monsters) > 0:
                if not self.fight(room.monsters):
                    continue

            output = ""

            if message != "":
                output += message

            output += "\n+----------------------------+"

            for y in range(-3, 4):
                row = ""
                row2 = ""

                for x in range(-3, 4):
                    room2 = self.get_room(self.px + x, self.py + y)

                    if room2:
                        if x == 0 and y == 0:
                            row += "@@"
                        else:
                            row += "██"

                        if room2.connections[1]:
                            row2 += "][  "
                        else:
                            row2 += "    "

                        if room2.connections[2] and x != -3:
                            row = row[:-4] + "==" + row[-2:]

                        if room2.connections[3]:
                            row += "=="
                        else:
                            row += "  "
                    else:
                        row += "    "
                        row2 += "    "

                output += "\n|" + row + "|"
                output += "\n|" + row2 + "|"

            output += "\n+----------------------------+"
            output += "\n" + room.get_desc()
            output += "\n"

            print(output)
            print("What to do? (w = north, s = south, a = east, d = west, q = other)")
            key = str(Getch.getch())[2:-1]

            old_x = self.px
            old_y = self.py

            self.px_old = old_x
            self.py_old = old_y

            if key == "w":
                if room.connections[0]:
                    message = "You move north."
                    self.py -= 1
                else:
                    message = "You can't move north."

            if key == "s":
                if room.connections[1]:
                    message = "You move south."
                    self.py += 1
                else:
                    message = "You can't move south."

            if key == "a":
                if room.connections[2]:
                    message = "You move west."
                    self.px -= 1
                else:
                    message = "You can't move west."

            if key == "d":
                if room.connections[3]:
                    message = "You move east."
                    self.px += 1
                else:
                    message = "You can't move east."

            if key == "q":
                actions = ["Inventory", "Inspect", "Interact", "Drop item", "Menu", "Back"]

                if room.room_type == "stair_room":
                    actions.append("Go down stairs")

                action = Utility.select_from_list(output + "\nWhat to do?", actions)

                match action:
                    case 0:
                        p = self.players[0] if len(self.players) == 1 else self.select_player(output)
                        stop = False
                        last_select = 0

                        while not stop:
                            items = []

                            for i in p.equipment:
                                items.append("@ " + i.get_name())

                            for i in p.inventory:
                                name = i.get_name()

                                if i.amount > 1:
                                    name += " x" + str(i.amount)

                                items.append(name)

                            weight = p.get_carrying_weight()
                            weight2 = p.get_carry_weight()

                            item = Utility.select_from_list(
                                output + "\nHere is your inventory. (" + str(weight) + "/" + str(weight2) + " lbs)",
                                items,
                                max_items=8, escapable=True, start=last_select
                            )

                            if item is not None:
                                message = p.use_item((p.equipment + p.inventory)[item])[1]
                                last_select = item

                                if message != "":
                                    Utility.clear()
                                    print(output)
                                    print(message)
                                    time.sleep(3)
                            else:
                                stop = True

                        continue

                    case 1:
                        p = self.players[0] if len(self.players) == 1 else self.select_player(output, include_dead=True)

                        Utility.clear()

                        print(output)
                        p.print_character()
                        input("Press enter to go continue.")
                        continue

                    case 2:
                        p = self.players[0] if len(self.players) == 1 else self.select_player(output)
                        last_select = 0

                        stop = False

                        while not stop:
                            stuff = room.containers + room.items
                            _list = []

                            for c in stuff:
                                if isinstance(c, Items.Item):
                                    name = c.get_name()

                                    if c.amount > 1:
                                        name += " x" + str(c.amount)

                                    _list.append(name)
                                else:
                                    if hasattr(c, "liquid"):
                                        _list.append(c.get_name())
                                    else:
                                        _list.append(c.get_name() + (" (empty)" if len(c.items) == 0 else ""))

                            item = Utility.select_from_list(output + "\nYou see these:", _list, max_items=8,
                                                            escapable=True, start=last_select)

                            if item is not None:
                                item2 = stuff[item]
                                last_select = item

                                if isinstance(item2, Items.Container):
                                    if hasattr(item2, "liquid"):
                                        if item2.liquid_amount <= 0:
                                            continue

                                        stop2 = False
                                        last_select = 0

                                        while not stop2:
                                            items = []

                                            for i in p.inventory:
                                                name = i.get_name()

                                                if i.amount > 1:
                                                    name += " x" + str(i.amount)

                                                items.append(name)

                                            item = Utility.select_from_list(
                                                output + "\nUse what to fill with " + item2.liquid + "?",
                                                items,
                                                max_items=8, escapable=True, start=last_select
                                            )

                                            if item is not None:
                                                item3 = p.inventory[item]

                                                if hasattr(item3, "liquid"):
                                                    amount = Utility.slider(output + "\nHow much?", 1, item2.liquid_amount, escapable=True)

                                                    if amount is not None:
                                                        result = item3.fill_with(item2.liquid, amount)

                                                        if len(result) == 3:
                                                            item2.liquid_amount -= result[2]

                                                        if result[0]:
                                                            stop2 = True

                                                        print(result[1])

                                                        time.sleep(3)
                                            else:
                                                stop2 = True

                                        continue
                                    else:
                                        if len(item2.items) == 0:
                                            continue

                                        stop2 = False
                                        last_select2 = 0

                                        while not stop2:
                                            _list2 = []

                                            for c in item2.items:
                                                name = c.get_name()

                                                if c.amount > 1:
                                                    name += " x" + str(c.amount)

                                                _list2.append(name)

                                            _item = Utility.select_from_list(
                                                output + "\nYou find these in " + item2.get_name() + ":", _list2,
                                                max_items=8, escapable=True, start=last_select2
                                            )

                                            if _item is not None:
                                                last_select2 = _item
                                                p.give(item2.items[_item])
                                                item2.items.pop(_item)
                                            else:
                                                stop2 = True

                                elif isinstance(item2, Items.Item):
                                    p.give(item2)
                                    room.items.pop(item - len(room.containers))
                            else:
                                stop = True

                        continue

                    case 3:
                        p = self.players[0] if len(self.players) == 1 else self.select_player(output)
                        stop = False
                        last_select = 0

                        while not stop:
                            items = []

                            for i in p.inventory:
                                name = i.get_name()

                                if i.amount > 1:
                                    name += " x" + str(i.amount)

                                items.append(name)

                            weight = p.get_carrying_weight()
                            weight2 = p.get_carry_weight()

                            item = Utility.select_from_list(
                                output + "\nWhat do you want to drop? (" + str(weight) + "/" + str(weight2) + " lbs)",
                                items,
                                max_items=8, escapable=True, start=last_select
                            )

                            if item is not None:
                                last_select = item

                                room.items.append(p.inventory[item])
                                p.inventory.pop(item)
                            else:
                                stop = True

                        continue

                    case 4:
                        item = Utility.select_from_list(output + "\nHere is the menu.", ["Exit game", "Close"])

                        if item == 0:
                            for p in self.players:
                                Creature.save_character(p)

                            exit(123)

                    case 5:
                        continue

                    case 6:
                        item = Utility.select_from_list(output + "\nGo down stairs? You can't come back.", ["Yes", "No"])

                        if item == 0:
                            self.load_level(self.level + 1)
                        else:
                            continue

            if not self.get_room(self.px, self.py):
                self.px = old_x
                self.py = old_y

    def fight(self, monsters):
        for p in self.players:
            p.pos = 3

        for m in monsters:
            m.pos = -3

        exp = 0

        while True:
            Utility.clear()

            alive = False

            for p in self.players:
                if p.health > 0:
                    alive = True

            if alive:
                for p in self.players:
                    if p.health <= 0:
                        continue

                    valid = False
                    msg = ""

                    while not valid:
                        if len(monsters) == 0:
                            output = []

                            for p2 in self.players:
                                p2.experience += round(max(exp / len(self.players), 1))
                                old_level = p2.level

                                while p2.experience >= p2.get_experience() and p2.level < 20:
                                    p2.experience -= p2.get_experience()
                                    p2.level += 1
                                    p.health = p2.get_health()

                                if p2.level != old_level:
                                    output.append(p2.get_name() + " leveled up to level " + str(p.level) + "!")

                            print("\n".join(output))
                            input("Press Enter to continue.")

                            return True

                        prompt = "Enemies"

                        for m in monsters:
                            prompt += "\n  " + m.get_name() + " [" + str(m.health) + "/" + str(m.get_health()) + "]"

                        prompt += "\n"
                        prompt += "\n" + p.name
                        prompt += "\n  Health: " + str(p.health) + "/" + str(p.get_health())
                        prompt += "\n  Spells: " + str(p.spell_slots) + "/" + str(p.get_spell_slots())
                        prompt += "\n--------------------------------"

                        actions = ["Attack with weapon", "Cast a spell", "Use an item", "Inspect", "Flee", "Pass"]

                        weapon_data = p.get_weapon_data()
                        weapon_name = Utility.get_name(weapon_data[0])

                        actions[0] = "Attack with " + weapon_name

                        action = Utility.select_from_list(prompt + "\nWhat will " + p.name + " do?", actions)

                        match action:
                            case 0:
                                can_attack = True
                                use_dex = False
                                data = Items.get_item_data(weapon_data[0])

                                if "ammunition" in data:
                                    if not p.has_item(data["ammunition"]):
                                        can_attack = False
                                    else:
                                        p.remove_item(data["ammunition"])

                                    use_dex = True

                                if can_attack:
                                    mons = []

                                    for m in monsters:
                                        if abs(m.pos - p.pos) <= 1 or weapon_data[3] == Items.ItemType.RangedWeapon:
                                            mons.append(m)

                                    target = self.select_monster(prompt, mons)

                                    if target is not None:
                                        Utility.clear()
                                        print(prompt)
                                        msg = self.combat_action(p, target, monsters, "melee", use_dex=use_dex)
                                        valid = True

                            case 1:
                                spells = p.get_spells()
                                spells2 = []

                                for s in spells:
                                    spells2.append(Utility.get_name(s))

                                spell = Utility.select_from_list(prompt + "\nYou know these spells:", spells2, max_items=8, escapable=True)

                                if spell is not None:
                                    spell2 = spells[spell]
                                    data = Skills.skills[spell2]

                                    target = None
                                    group = monsters

                                    if "target" in data and data["target"] != Skills.TargetType.Enemies:
                                        if data["target"] == Skills.TargetType.Allies:
                                            target = self.players.index(self.select_player(prompt, True))
                                        else:
                                            target = self.players.index(p)

                                        group = self.players
                                    else:
                                        target = self.select_monster(prompt, group, pos=p.pos)

                                    if target is not None:
                                        can_attack = True

                                        if abs(group[target].pos - p.pos) > 1:
                                            if "range" in data and data["range"] == "melee":
                                                msg = "Out of range."
                                                can_attack = False

                                        if can_attack:
                                            msg = self.combat_action(p, target, group, spell2)
                                            valid = True

                            case 2:
                                items = []

                                for i in p.inventory:
                                    name = i.get_name()

                                    if i.amount > 1:
                                        name += " x" + str(i.amount)

                                    items.append(name)

                                item = Utility.select_from_list(prompt + "\nHere is your inventory.", items, max_items=8, escapable=True)

                                if item is not None:
                                    message = p.use_item(p.inventory[item])

                                    msg = message[1]
                                    valid = message[0]

                            case 3:
                                Utility.clear()
                                p.print_character()
                                input("Press enter to continue.")

                            case 4:
                                self.px = self.px_old
                                self.py = self.py_old

                                return False

                            case 5:
                                valid = True
                                continue

                        if msg != "":
                            Utility.clear()
                            print(prompt)
                            print(msg)
                            time.sleep(3)
                            msg = ""

                    # clean up dead monsters
                    for i in range(20):
                        for m in range(len(monsters)):
                            if monsters[m].health <= 0:
                                corpse = Items.Container("corpse", monsters[m].equipment, special_name=monsters[m].get_name() + "'s Corpse")
                                self.get_room(self.px, self.py).containers.append(corpse)
                                exp += monsters[m].get_experience()
                                del monsters[m]
                                break

                log = []

                for m in monsters:
                    prompt = "Enemies"

                    for m2 in monsters:
                        prompt += "\n  " + m2.get_name() + " [" + str(m2.health) + "/" + str(m2.get_health()) + "]"

                    prompt += "\n"
                    prompt += "\n--------------------------------"

                    attacks = Monsters.monsters[m.id]["attacks"]
                    attack = random.choice(attacks)
                    target = random.choice(self.players)

                    if abs(m.pos - target.pos) > 1 and "range" in Skills.skills[attack] and Skills.skills[attack]["range"] == "melee":
                        if random.randint(1, 3) == 1 or m.get_stat("dex") >= 8:
                            log.append(m.get_name() + " moves closer to " + target.get_name() + "!")

                            if target.pos > m.pos:
                                m.pos += 1
                            else:
                                m.pos -= 1
                    else:
                        log.append(self.combat_action(m, self.players.index(target), self.players, attack))

                    Utility.clear()
                    print(prompt)

                    for msg in log:
                        print(msg)

                    time.sleep(1)

                time.sleep(4)
            else:
                self.game_over()
                return

    def get_room(self, x, y):
        if 0 <= x < 21 and 0 <= y < 21:
            return self.map[y][x]
        else:
            return None

    def set_room(self, x, y, _id):
        if 0 <= x < 21 and 0 <= y < 21:
            room = Rooms.Room(_id)
            room.create_items(self.level, self.difficulty_multiplier)
            room.create_monsters(self.theme, self.level, self.difficulty_multiplier)

            self.map[y][x] = room

    def set_room2(self, x, y, x2, y2, _id):
        if 0 <= x + x2 < 21 and 0 <= y + y2 < 21:
            room = self.get_room(x + x2, y + y2)

            if not room:
                room = Rooms.Room(_id)
                room.create_items(self.level, self.difficulty_multiplier)
                room.create_monsters(self.theme, self.level, self.difficulty_multiplier)

                self.map[y + y2][x + x2] = room

            if y2 == 1:
                room.connections[0] = True

            if y2 == -1:
                room.connections[1] = True

            if x2 == 1:
                room.connections[2] = True

            if x2 == -1:
                room.connections[3] = True

    def spread_rooms(self, iterations):
        ready = []

        for i in range(21):
            ready.append([False] * 21)

        for i in range(iterations):
            for y in range(21):
                for x in range(21):
                    if self.get_room(x, y) and not self.map2[y][x] and ready[y][x]:
                        room = self.get_room(x, y)
                        connections = room.connections
                        doors = []
                        doors2 = []

                        for i2 in range(4):
                            if not connections[i2]:
                                doors.append(random.randint(1, 5) == 1)
                                doors2.append(i2)
                            else:
                                doors.append(True)

                        doors[random.choice(doors2)] = True

                        if doors[0]:
                            self.set_room2(x, y, 0, -1, room.get_next_id())

                        if doors[1]:
                            self.set_room2(x, y, 0, 1, room.get_next_id())

                        if doors[2]:
                            self.set_room2(x, y, -1, 0, room.get_next_id())

                        if doors[3]:
                            self.set_room2(x, y, 1, 0, room.get_next_id())

                        for c in range(4):
                            if doors[c]:
                                room.connections[c] = True

                        self.map2[y][x] = True

            for y in range(21):
                for x in range(21):
                    if self.get_room(x, y):
                        ready[y][x] = True

    def combat_action(self, user, index, group, skill_id, use_dex=False):
        data = Skills.skills[skill_id]
        output = []
        targets = []

        if "area" in data:
            for c in group:
                if abs(group[index].pos - c.pos) <= data["area"]:
                    targets.append(c)

            if group[index] not in targets:
                targets.append(group[index])
        else:
            targets.append(group[index])

        for target in targets:
            if "damage" in data:
                if skill_id == "melee" or skill_id == "claw" or skill_id == "slam":
                    weapon_data = user.get_weapon_data()
                    weapon_name = Utility.get_name(weapon_data[0])

                    damage = max(round(
                        weapon_data[1] * random.uniform(0.5, 1.5)) + (user.get_stat_modifier("dex") if use_dex else user.get_stat_modifier("str")
                    ), 1)
                    dmg = str(target.damage(damage, weapon_data[2])) + " " + weapon_data[2].name.lower()

                    output.append(user.get_name() + " attacks " + target.get_name() + ", dealing " + dmg + " using " + weapon_name + ".")
                else:
                    spell_name = Utility.get_name(skill_id)

                    damage = max(round(data["damage"] * random.uniform(0.5, 1.5)) + user.get_stat_modifier("spellcasting"), 1)
                    dmg = str(target.damage(damage, data["damage_type"])) + " " + data["damage_type"].name.lower()

                    output.append(user.get_name() + " casts " + spell_name + " on " + target.get_name() + ", dealing " + dmg + ".")

                if target.health <= 0:
                    output.append(target.get_name() + " died!")

            if "condition" in data:
                target.add_condition(data["condition"])

        return "\n".join(output)

    def select_player(self, output, include_dead=False):
        names = []
        players = []

        for p in self.players:
            if p.health > 0 or include_dead:
                players.append(p)
                names.append(p.get_name())

        return players[Utility.select_from_list(output + "\nWho?", names)]

    def select_monster(self, output, monsters, pos=100):
        targets = []

        for m in monsters:
            if pos != 100:
                targets.append(m.get_name() + " [" + str(abs(m.pos - pos)) + "m]")
            else:
                targets.append(m.get_name())

        return Utility.select_from_list(output + "\nTarget who?", targets, max_items=8, escapable=True)

    def game_over(self):
        Utility.clear()

        big_title = [
            "#####   #   #   # #####   ##### #   # ##### ###   ##",
            "#      # #  ## ## #       #   # #   # #     #  #  ##",
            "# ###  ###  # # # ###     #   #  # #  ###   ####  ##",
            "#   # #   # #   # #       #   #  # #  #     # #",
            "##### #   # #   # #####   #####   #   ##### #  ## ##",
        ]

        for i in big_title:
            print(i.replace("#", "█"))

        print()
        print("Oh no! Everyone died!")
        exit(123)
