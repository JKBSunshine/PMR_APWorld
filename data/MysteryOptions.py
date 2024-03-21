# from PMR: https://github.com/icebound777/PMR-SeedGenerator/blob/main/models/options/MysteryOptionSet.py
from .ItemList import item_table


# original items are, in order: mushroom, super shroom, fire flower, stone cap, dizzy dial, thunder rage, pebble
class MysteryOptions:
    def __init__(self):
        self.mystery_random_choice = 0
        self.mystery_random_pick = False
        self.mystery_itemA = [name for name, values in item_table.items() if values[2] == 138][0]
        self.mystery_itemB = [name for name, values in item_table.items() if values[2] == 140][0]
        self.mystery_itemC = [name for name, values in item_table.items() if values[2] == 128][0]
        self.mystery_itemD = [name for name, values in item_table.items() if values[2] == 136][0]
        self.mystery_itemE = [name for name, values in item_table.items() if values[2] == 154][0]
        self.mystery_itemF = [name for name, values in item_table.items() if values[2] == 130][0]
        self.mystery_itemG = [name for name, values in item_table.items() if values[2] == 133][0]
