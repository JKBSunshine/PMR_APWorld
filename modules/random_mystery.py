# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_mystery.py
# modified slightly to use the item table instead of db
import random

from ..options import MysteryShuffle
from ..data.ItemList import item_table
from ..data.MysteryOptions import MysteryOptions


def get_random_mystery(mystery_option: MysteryShuffle) -> MysteryOptions:
    mystery_settings = MysteryOptions()

    # If Random Choice is on, then none of the other settings matter
    if mystery_option == MysteryShuffle.option_Random_Per_Use:
        return mystery_settings

    if mystery_option == MysteryShuffle.option_Random_Pick:
        # Set possible items the same as Random Choice (see Item_Mystery.bpat)
        possible_items = []
        chosen_items = []

        mystery_itemid = item_table["Mystery"][2]

        possible_items.extend(4 * [item_table["Mushroom"][2]])
        possible_items.extend(2 * [item_table["SuperShroom"][2]])
        possible_items.extend(1 * [item_table["UltraShroom"][2]])
        possible_items.extend(4 * [item_table["HoneySyrup"][2]])
        possible_items.extend(2 * [item_table["MapleSyrup"][2]])
        possible_items.extend(1 * [item_table["JamminJelly"][2]])
        possible_items.extend(2 * [item_table["POWBlock"][2]])
        possible_items.extend(2 * [item_table["FireFlower"][2]])
        possible_items.extend(2 * [item_table["SnowmanDoll"][2]])
        possible_items.extend(2 * [item_table["ThunderRage"][2]])
        possible_items.extend(2 * [item_table["ShootingStar"][2]])
        possible_items.extend(2 * [item_table["Pebble"][2]])
        possible_items.extend(2 * [item_table["Coconut"][2]])
        possible_items.extend(2 * [item_table["ThunderBolt"][2]])
        possible_items.extend(2 * [item_table["EggMissile"][2]])
        possible_items.extend(2 * [item_table["SleepySheep"][2]])
        possible_items.extend(2 * [item_table["DizzyDial"][2]])
        possible_items.extend(2 * [item_table["StopWatch"][2]])
        possible_items.extend(2 * [item_table["VoltShroom"][2]])
        possible_items.extend(2 * [item_table["StoneCap"][2]])
        possible_items.extend(1 * [item_table["RepelGel"][2]])
        possible_items.extend(4 * [mystery_itemid])

        # We have 7 item slots to fill, with the first one having a hardcoded
        # double-chance of occurring
        while len(chosen_items) < 7:
            random_item = random.choice(possible_items)
            if not (random_item == mystery_itemid and len([x for x in chosen_items if x == mystery_itemid]) >= 4):
                chosen_items.append(random_item)
            if chosen_items[0] == mystery_itemid:
                chosen_items.pop(0)

        mystery_settings.mystery_itemA = chosen_items[0]
        mystery_settings.mystery_itemB = chosen_items[1]
        mystery_settings.mystery_itemC = chosen_items[2]
        mystery_settings.mystery_itemD = chosen_items[3]
        mystery_settings.mystery_itemE = chosen_items[4]
        mystery_settings.mystery_itemF = chosen_items[5]
        mystery_settings.mystery_itemG = chosen_items[6]

    else:
        # Set vanilla
        mystery_settings.mystery_itemA = item_table["Mushroom"][2]
        mystery_settings.mystery_itemB = item_table["SuperShroom"][2]
        mystery_settings.mystery_itemC = item_table["FireFlower"][2]
        mystery_settings.mystery_itemD = item_table["StoneCap"][2]
        mystery_settings.mystery_itemE = item_table["DizzyDial"][2]
        mystery_settings.mystery_itemF = item_table["ThunderRage"][2]
        mystery_settings.mystery_itemG = item_table["Pebble"][2]

    return mystery_settings
