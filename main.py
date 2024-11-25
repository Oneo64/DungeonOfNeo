import time

import Creature
import Game
import Utility

import os


big_title = [
    "###   #   # #   # ##### ##### ##### #   #",
    "#  #  #   # ##  # #     #     #   # ##  #",
    "#   # #   # # # # # ### ###   #   # # # #",
    "#  #  #   # #  ## #   # #     #   # #  ##",
    "###   ##### #   # ##### ##### ##### #   #",
    "",
    "   ##### #####      #   # ##### #####",
    "   #   # #          ##  # #     #   #",
    "   #   # ###        # # # ###   #   #",
    "   #   # #          #  ## #     #   #",
    "   ##### #          #   # ##### #####"
]

big_title2 = big_title
big_title_str = ""

for i in big_title2:
    big_title_str += i.replace("#", "█")
    big_title_str += "\n"

if __name__ == "__main__":
    for shade in range(0, 5):
        time.sleep(0.5)
        Utility.clear()

        for i in big_title:
            shade_block = " "

            if shade == 1:
                shade_block = "░"

            if shade == 2:
                shade_block = "▒"

            if shade == 3:
                shade_block = "▓"

            if shade == 4:
                shade_block = "█"

            print(i.replace("#", shade_block))

    time.sleep(3)

    print()
    print("W/S to move up/down a list.")
    print("Lists look like this:")
    print("  > Item a")
    print("  Item b")
    print("  Item c")
    print()
    print("A/D to increase/decrease the value of a slider.")
    print("Sliders look like this:")
    print("  1 ====|----- 10 (5)")
    print()
    print("Some spells and monsters may be taken from: https://dnd.wizards.com/resources/systems-reference-document.")
    print("It is licenced by creative commons 4.0:     https://creativecommons.org/licenses/by/4.0/legalcode")
    print("NOTE: For saves to load and not crash the game, run this using the terminal.")
    input("Press enter to continue.")

    title = big_title_str + "\nDifficulty?"
    difficulty = Utility.select_from_list(title, ["easy", "medium", "hard"])

    players = []

    while len(players) < 5:
        title = big_title_str + "\nParty"

        for p in range(5):
            if p < len(players):
                title += "\n  > " + players[p].name
            else:
                title += "\n  > Empty Character"

        title += "\n--------------------------------"

        if len(players) > 0:
            Utility.clear()

            if Utility.select_from_list(title + "\nDo you want to add another character?", ["yes", "no"]) == 1:
                break

        if Utility.select_from_list(title, ["Create new character", "Load character"]) == 0:
            races = ["dwarf", "elf", "human", "gnome"]
            race = races[Utility.select_from_list(title + "\nChoose a race:", races)]

            classes = ["druid", "fighter", "ranger", "rogue", "paladin", "warlock", "wizard"]
            player_class = classes[Utility.select_from_list(title + "\nChoose a class:", classes)]

            player = Creature.Creature([input("You shall be known as: "), race, player_class])

            Creature.save_character(player)

            if Utility.select_from_list(title + "\nCreate this character?", ["yes", "no"]) == 0:
                players.append(player)
        else:
            files = os.listdir("saves")
            available_files = []
            chosen_files = []

            for f in files:
                if f.endswith(".json") and f not in chosen_files:
                    available_files.append(f)

            file = Utility.select_from_list(title + "\nHere are all the saves. (root/saves/example.json)", available_files, escapable=True)

            if file is not None:
                data = available_files[file]
                player = Creature.load_character(data)

                chosen_files.append(data)

                players.append(player)

    game = Game.Game("demon_lord", players, difficulty)
    game.game_loop()
