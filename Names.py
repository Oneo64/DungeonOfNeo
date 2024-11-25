import random
import time

table = {
    "demon_lord": [
        ["baa", "nir", "isl", "tar", "lee", "lal", "hoz", "mef", "dag", "grod", "het", "grd", "vam", "tui", "puud", "ras"],
        ["kan", "gob", "lud", "de", "vo", "sed", "gee", "no", "ree", "fhed", "jar", "bu", "bel", "ru", "po", "vnk", "taa"],
        ["ghad", "ghron", "teg", "zho", "aat", "mrd", "mag", "tuo", "zhem", "zok", "rod", "ta", "ni", "gar", "gro", "rterd"]
    ],
    "blob": [
        ["glob", "glop", "plog", "gub", "grub", "greeb", "ga", "blo", "gla"],
        ["glo", "go", "golo", "gro", "gab", "glab", "galb", "bag", "flog"],
        ["gab", "grob", "garb", "gabab", "blab", "gagab", "blob", "baba", "glop"],
        ["galab", "lababab", "gabag", "garbag", "bag", "fag", "gababa", "pog"]
    ]
}


def generate(category):
    t = table[category]
    n = random.choice(t[0])

    if random.randint(1, 3) == 1:
        n += random.choice(t[1] + t[2])
    else:
        n += random.choice(t[1]) + random.choice(t[2])

    return n


def generate2(category):
    t = table[category]
    n = ""

    for i in t:
        n += random.choice(i)

    return n
