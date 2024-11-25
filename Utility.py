import math
import os
import Getch


def print_items(items):
    for i in items:
        print(i.id)


def clear():
    try:
        os.system("cls")
    except:
        os.system("clear")


def get_name(txt):
    return txt.replace("_", " ").title().replace("Of ", "of ").replace("The ", "the ")


def multiplier(level, difficulty):
    return math.ceil(difficulty * (0.5 + (level * 0.5)))


def select_from_list(prompt, _list, max_items=0, escapable=False, start=0):
    i = start
    page = 0

    while True:
        clear()
        print(prompt)

        if max_items == 0:
            for d in range(len(_list)):
                if i == d:
                    print("  > " + _list[d])
                else:
                    print("  " + _list[d])
        else:
            for d in range(page * max_items, min((page + 1) * max_items, len(_list))):
                if i == d:
                    print("  > " + _list[d])
                else:
                    print("  " + _list[d])

            if page == math.floor(len(_list) / max_items):
                for i2 in range(1 - (len(_list) % max_items)):
                    print()

            print("  --------------------------------")
            print("  Page " + str(page + 1) + " of " + str(math.floor(len(_list) / max_items) + 1))

        if escapable:
            print("  Press [Q] to cancel.")

        key = str(Getch.getch())[2:-1]

        if key == "w":
            i -= 1

        if key == "s":
            i += 1

        if escapable and key == "q":
            return None

        if max_items > 0:
            change = False

            if key == "d":
                page += 1
                change = True

            if key == "a":
                page -= 1
                change = True

            if page < 0:
                page = 0

            if page > math.floor(len(_list) / max_items):
                page = math.floor(len(_list) / max_items)

            if change:
                i = page * max_items
            else:
                if i < page * max_items:
                    i = page * max_items

                if i >= min((page + 1) * max_items, len(_list)):
                    i = min((page + 1) * max_items, len(_list)) - 1
        else:
            i = min(max(i, 0), len(_list) - 1)

        if key == "\\r":
            if len(_list) == 0:
                return None
            else:
                return i


def slider(prompt, _min, _max, escapable=False, start=0):
    i = max(start, _min)

    while True:
        clear()
        print(prompt)

        bar = ""

        for i2 in range(i - _min + 1):
            if i2 == i - _min:
                bar += "|"
            else:
                bar += "="

        for i2 in range(_max - _min - i + 1):
            bar += "-"

        print(str(_min) + " " + bar + " " + str(_max) + " (" + str(i) + ")")

        if escapable:
            print("  Press [Q] to cancel.")

        key = str(Getch.getch())[2:-1]

        if key == "d":
            i += 1

        if key == "a":
            i -= 1

        if escapable and key == "q":
            return None

        i = min(max(i, _min), _max)

        if key == "\\r":
            return i
