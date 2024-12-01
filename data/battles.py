# name, vanilla battle id

boss_battles = {
    "KoopaBros": 1792,
    "Tutankoopa": 3072,
    "TubbasHeart": 3599,
    "GeneralGuy": 4352,
    "LavaPiranha": 5888,
    "HuffnPuff": 6400,
    "CrystalKing": 8192,
}


def get_battle_key(name):
    return 0xA9 << 24 | boss_battles[name]
