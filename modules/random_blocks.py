# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_blocks.py
# modified to pull blocks from locations list instead of db table
"""
This module can modify the placement of different block types within the world.
"""

import random

from ..data.enum_types import BlockType
from ..data.LocationsList import location_groups
from ..Locations import PMLocation


def get_key(blockdata):
    return (0xA1 << 24) | (blockdata[0] << 16) | (blockdata[1] << 8) | blockdata[2]


def get_block_placement(
    shuffle_blocks: bool,
    supers_are_yellow: bool
):
    block_placement = []

    # make list of blocks to shuffle, taking care to change supers to normal item blocks if that setting is on
    if not shuffle_blocks:
        for block, data in block_table.items():

            if data[4] == BlockType.SUPER and supers_are_yellow:
                block_placement.append((get_key(data), BlockType.YELLOW))
            else:
                block_placement.append((get_key(data), data[4]))
    else:
        db_keys = {}
        db_values = {}
        for block, data in block_table.items():
            key = get_key(data)
            area_id = (key & 0xFF0000) >> 16
            if area_id not in db_keys:
                db_keys[area_id] = [key]
            else:
                db_keys[area_id].append(key)

            if data[4] == BlockType.SUPER and supers_are_yellow:
                block_type = BlockType.YELLOW
            else:
                block_type = data[4]

            if block_type not in db_values:
                db_values[block_type] = 1
            else:
                db_values[block_type] = db_values[block_type] + 1

        block_type_supers = BlockType.SUPER if not supers_are_yellow else BlockType.YELLOW

        while (block_type_supers in db_values) and db_keys:
            # Choose random area, then random db key / block spawn in that area
            area_id = random.choice(list(db_keys))
            db_key = random.choice(db_keys[area_id])
            db_keys[area_id].remove(db_key)
            if not db_keys[area_id]:
                db_keys.pop(area_id)

            block_placement.append((db_key, block_type_supers))

            db_values[block_type_supers] = db_values[block_type_supers] - 1
            if db_values[block_type_supers] == 0:
                db_values.pop(block_type_supers)

    return block_placement


#  id      area     map     index         name      vanilla type (0 is multi, 1 is super)
block_table = {
    1:      (0,      3,      64,     "RandomBlockA", 0),
    2:      (1,      6,      64,     "RandomBlockA", 0),
    3:      (2,      6,      64,     "RandomBlockA", 1),
    4:      (2,      9,      64,     "RandomBlockA", 1),
    5:      (2,      10,     64,     "RandomBlockA", 1),
    6:      (2,      13,     64,     "RandomBlockA", 1),
    7:      (2,      14,     64,     "RandomBlockA", 0),
    8:      (2,      15,     64,     "RandomBlockA", 1),
    9:      (6,      5,      64,     "RandomBlockA", 0),
    10:     (8,      5,      64,     "RandomBlockA", 1),
    11:     (10,     6,      64,     "RandomBlockA", 0),
    12:     (10,     11,     64,     "RandomBlockA", 0),
    13:     (10,     19,     64,     "RandomBlockA", 0),
    14:     (10,     19,     65,     "RandomBlockB", 0),
    15:     (10,     28,     64,     "RandomBlockA", 0),
    16:     (10,     37,     64,     "RandomBlockA", 0),
    17:     (10,     40,     64,     "RandomBlockA", 0),
    18:     (10,     41,     64,     "RandomBlockA", 1),
    19:     (10,     48,     64,     "RandomBlockA", 0),
    20:     (10,     48,     65,     "RandomBlockB", 0),
    21:     (10,     48,     66,     "RandomBlockC", 0),
    22:     (10,     48,     67,     "RandomBlockD", 0),
    23:     (10,     48,     68,     "RandomBlockE", 0),
    24:     (10,     48,     69,     "RandomBlockF", 0),
    25:     (11,     9,      64,     "RandomBlockA", 1),
    26:     (14,     2,      64,     "RandomBlockA", 0),
    27:     (15,     4,      64,     "RandomBlockA", 1),
    28:     (16,     8,      64,     "RandomBlockA", 0),
    29:     (16,     10,     64,     "RandomBlockA", 1),
    30:     (16,     10,     65,     "RandomBlockB", 0),
    31:     (16,     16,     64,     "RandomBlockA", 0),
    32:     (17,     8,      64,     "RandomBlockA", 1),
    33:     (18,     3,      64,     "RandomBlockA", 1),
    34:     (18,     8,      64,     "RandomBlockA", 1),
    35:     (19,     3,      64,     "RandomBlockA", 1),
    36:     (19,     6,      64,     "RandomBlockA", 0),
    37:     (19,     11,     64,     "RandomBlockA", 1),
    38:     (20,     7,      64,     "RandomBlockA", 1),
    39:     (21,     11,     64,     "RandomBlockA", 0),
    40:     (21,     11,     65,     "RandomBlockB", 0)
}
