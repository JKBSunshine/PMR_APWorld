# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_battles.py

from ..data.battles import get_battle_key, boss_battles
from ..data.formations_meta import chapter_battle_mapping
from ..options import BossShuffle


def get_boss_battles(boss_shuffle: int, random) -> tuple[list[tuple[int, int]], dict[int, int]]:
    def get_battle_group(battle: int) -> int:
        # battles have two bytes, the upper byte signifies the battle group
        # to load, the lower byte the id within that group
        return battle >> 8

    def get_battle_chapter(battle_group: int) -> int | None:
        for chapter, battle_group_list in chapter_battle_mapping.items():
            if battle_group in [int(x, 16) for x in battle_group_list]:
                return chapter
        return None
    battles_setup: list[tuple[int, int]] = []
    boss_chapter_map: dict[int, int] = {}

    if boss_shuffle == BossShuffle.option_false:
        for name, vanilla_id in boss_battles.items():
            battles_setup.append((get_battle_key(name), vanilla_id))
        boss_chapter_map = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}  # default

    elif boss_shuffle == BossShuffle.option_true:
        keys_chapters: list = []
        values_chapters: list[tuple[int, int]] = []

        for name, vanilla_id in boss_battles.items():
            key = get_battle_key(name)

            battle_group = get_battle_group(vanilla_id)
            chapter = get_battle_chapter(battle_group)
            assert (chapter is not None)

            keys_chapters.append((key, chapter))
            values_chapters.append((vanilla_id, chapter))

        random.shuffle(values_chapters)

        battles_setup: list[tuple[int, int]] = list(zip(
            [x[0] for x in keys_chapters], [x[0] for x in values_chapters]
        ))
        boss_chapter_map: dict[int, int] = dict(zip(
            [x[1] for x in values_chapters], [x[1] for x in keys_chapters]
        ))  # e.g. General Guy appears in chapter 1, so (4, 1)

    return battles_setup, boss_chapter_map
