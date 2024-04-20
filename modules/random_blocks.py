# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_blocks.py
# modified to pull blocks from locations list instead of db table
"""
This module can modify the placement of different block types within the world.
"""

import random

from ..data.enum_types import BlockType
from ..data.LocationsList import location_groups
from ..Locations import PMLocation


def get_block_key(block_name):
    block_data = block_table[block_name]
    return (0xA1 << 24) | (block_data[0] << 16) | (block_data[1] << 8) | block_data[2]


def get_block_placement(
    shuffle_blocks: bool,
    supers_are_yellow: bool
):
    block_placement = []
    block_names = []
    block_values = []
    # make list of blocks to shuffle, taking care to change supers to normal item blocks if that setting is on
    for block, data in block_table.items():
        block_names.append(block)
        if data[4] == BlockType.SUPER and supers_are_yellow:
            block_values.append(2)  # BlockType.YELLOW
        else:
            block_values.append(data[4])

    if shuffle_blocks:
        random.shuffle(block_values)

    return dict(zip(block_names, block_values))


#                                              (0 is multi, 1 is super)
#  id      area     map     index         name    vanilla type               location name
block_table = {
    "GR Jr. Troopa's Playground In MultiCoinBlock":            (0,      3,      64,     "RandomBlockA",    0),
    "TT Port District In MultiCoinBlock":                      (1,      6,      64,     "RandomBlockA",    0),
    "TTT Elevator Attic Room (B2) In SuperBlock":              (2,      6,      64,     "RandomBlockA",    1),
    "TTT Blue Pushblock Room (B2) In SuperBlock":              (2,      9,      64,     "RandomBlockA",    1),
    "TTT Metal Block Room (B3) In SuperBlock":                 (2,      10,     64,     "RandomBlockA",    1),
    "TTT Frozen Room (B3) In SuperBlock":                      (2,      13,     64,     "RandomBlockA",    1),
    "TTT Hall to Blooper 1 (B1) In MultiCoinBlock":            (2,      14,     64,     "RandomBlockA",    0),
    "TTT Under the Toad Town Pond In SuperBlock":              (2,      15,     64,     "RandomBlockA",    1),
    "KR Pleasant Path Bridge In MultiCoinBlock":               (6,      5,      64,     "RandomBlockA",    0),
    "MR Train Station In SuperBlock":                          (8,      5,      64,     "RandomBlockA",    1),
    "DDD N3E3 In MultiCoinBlock":                              (10,     6,      64,     "RandomBlockA",    0),
    "DDD N2E1 (Tweester A) In MultiCoinBlock":                 (10,     11,     64,     "RandomBlockA",    0),
    "DDD N1E2 In MultiCoinBlock Center":                       (10,     19,     64,     "RandomBlockA",    0),
    "DDD N1E2 In MultiCoinBlock Bottom Right":                 (10,     19,     65,     "RandomBlockB",    0),
    "DDD S1W3 In MultiCoinBlock Top Left":                     (10,     28,     64,     "RandomBlockA",    0),
    "DDD S2W1 In MultiCoinBlock Top":                          (10,     37,     64,     "RandomBlockA",    0),
    "DDD S2E2 West of Oasis In MultiCoinBlock":                (10,     40,     64,     "RandomBlockA",    0),
    "DDD S2E3 Oasis In SuperBlock":                            (10,     41,     64,     "RandomBlockA",    1),
    "DDD S3E3 South of Oasis In MultiCoinBlock Top Left":      (10,     48,     64,     "RandomBlockA",    0),
    "DDD S3E3 South of Oasis In MultiCoinBlock Top Right":     (10,     48,     65,     "RandomBlockB",    0),
    "DDD S3E3 South of Oasis In MultiCoinBlock Right":         (10,     48,     66,     "RandomBlockC",    0),
    "DDD S3E3 South of Oasis In MultiCoinBlock Left":          (10,     48,     67,     "RandomBlockD",    0),
    "DDD S3E3 South of Oasis In MultiCoinBlock Bottom Left":   (10,     48,     68,     "RandomBlockE",    0),
    "DDD S3E3 South of Oasis In MultiCoinBlock Bottom Right":  (10,     48,     69,     "RandomBlockF",    0),
    "DDR Vertical Shaft In SuperBlock":                        (11,     9,      64,     "RandomBlockA",    1),
    "GG Wasteland Ascent 2 In MultiCoinBlock":                 (14,     2,      64,     "RandomBlockA",    0),
    "TC Stairs to Basement In SuperBlock":                     (15,     4,      64,     "RandomBlockA",    1),
    "SGT GRN Treadmills/Slot Machine In MultiCoinBlock":       (16,     8,      64,     "RandomBlockA",    0),
    "SGT RED Moving Platforms In SuperBlock":                  (16,     10,     64,     "RandomBlockA",    1),
    "SGT RED Moving Platforms In MultiCoinBlock":              (16,     10,     65,     "RandomBlockB",    0),
    "SGT PNK Tracks Hallway In MultiCoinBlock":                (16,     16,     64,     "RandomBlockA",    0),
    "JJ SW Jungle (Super Block) In SuperBlock":                (17,     8,      64,     "RandomBlockA",    1),
    "MLL Fire Bar Bridge In SuperBlock":                       (18,     3,      64,     "RandomBlockA",    1),
    "MLL Zipline Cavern In SuperBlock":                        (18,     8,      64,     "RandomBlockA",    1),
    "FLO (SE) Briar Platforming In SuperBlock":                (19,     3,      64,     "RandomBlockA",    1),
    "FLO (West) Maze In MultiCoinBlock":                       (19,     6,      64,     "RandomBlockA",    0),
    "FLO (NE) Elevators In SuperBlock":                        (19,     11,     64,     "RandomBlockA",    1),
    "SR Shiver Mountain Hills In SuperBlock":                  (20,     7,      64,     "RandomBlockA",    1),
    "CP Blue Mirror Hall 2 In MultiCoinBlock Front":           (21,     11,     64,     "RandomBlockA",    0),
    "CP Blue Mirror Hall 2 In MultiCoinBlock Back":            (21,     11,     65,     "RandomBlockB",    0)
}
