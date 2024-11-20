# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_quizzes.py
"""
This module is used for modifying the questions asked by Chuck Quizmo in
various areas of the game.
"""


def get_randomized_quizzes(random) -> list:
    """
    Returns a list of tuples where the first value holds the dbkey for a quiz
    question and the second value holds the shuffled quiz question index. Also
    includes key/value pairs for the number of questions per area.
    """
    quiz_list = []
    db_keys = []
    db_values = []

    for name, data in quiz_table.items():
        db_keys.append(get_key(name))
        db_values.append(data[4])

    random.shuffle(db_values)

    for db_key, db_value in zip(db_keys, db_values):
        quiz_list.append((db_key, db_value))

    return quiz_list


# get the address for the given option using its key type (0xAF), area, map, and index
def get_key(quiz_name):
    data = quiz_table[quiz_name]
    return (0xAF << 24) | (data[1] << 16) | (data[2] << 8) | data[3]


#    Name     id    area     map    index   default val
quiz_table = {
    "MAC_00": (1,      3,      0,      0,     7),
    "MAC_01": (2,      3,      0,      1,     10),
    "MAC_02": (3,      3,      0,      2,     30),
    "MAC_03": (4,      3,      0,      3,     22),
    "MAC_04": (5,      3,      0,      4,     31),
    "MAC_05": (6,      3,      0,      5,     42),
    "MAC_06": (7,      3,      0,      6,     35),
    "MAC_07": (8,      3,      0,      7,     57),
    "MAC_08": (9,      3,      0,      8,     52),
    "MAC_09": (10,     3,      0,      9,     48),
    "MAC_0A": (11,     3,      0,      10,    41),
    "MAC_0B": (12,     3,      0,      11,    37),
    "MAC_0C": (13,     3,      0,      12,    25),
    "MAC_0D": (14,     3,      0,      13,    53),
    "MAC_0E": (15,     3,      0,      14,    51),
    "MAC_0F": (16,     3,      0,      15,    17),
    "KMR_00": (17,     3,      1,      0,     4),
    "KMR_01": (18,     3,      1,      1,     8),
    "KMR_02": (19,     3,      1,      2,     2),
    "KMR_03": (20,     3,      1,      3,     5),
    "KMR_04": (21,     3,      1,      4,     1),
    "KMR_05": (22,     3,      1,      5,     6),
    "KMR_06": (23,     3,      1,      6,     0),
    "KMR_07": (24,     3,      1,      7,     3),
    "NOK_00": (25,     3,      2,      0,     11),
    "NOK_01": (26,     3,      2,      1,     12),
    "NOK_02": (27,     3,      2,      2,     13),
    "NOK_03": (28,     3,      2,      3,     18),
    "NOK_04": (29,     3,      2,      4,     20),
    "NOK_05": (30,     3,      2,      5,     24),
    "NOK_06": (31,     3,      2,      6,     19),
    "NOK_07": (32,     3,      2,      7,     15),
    "DRO_00": (33,     3,      3,      0,     21),
    "DRO_01": (34,     3,      3,      1,     26),
    "DRO_02": (35,     3,      3,      2,     27),
    "DRO_03": (36,     3,      3,      3,     29),
    "DRO_04": (37,     3,      3,      4,     56),
    "DRO_05": (38,     3,      3,      5,     33),
    "DRO_06": (39,     3,      3,      6,     34),
    "DRO_07": (40,     3,      3,      7,     39),
    "JAN_00": (41,     3,      4,      0,     46),
    "JAN_01": (42,     3,      4,      1,     45),
    "JAN_02": (43,     3,      4,      2,     43),
    "JAN_03": (44,     3,      4,      3,     50),
    "JAN_04": (45,     3,      4,      4,     47),
    "JAN_05": (46,     3,      4,      5,     49),
    "JAN_06": (47,     3,      4,      6,     58),
    "JAN_07": (48,     3,      4,      7,     44),
    "SAM_00": (49,     3,      5,      0,     16),
    "SAM_01": (50,     3,      5,      1,     59),
    "SAM_02": (51,     3,      5,      2,     23),
    "SAM_03": (52,     3,      5,      3,     32),
    "SAM_04": (53,     3,      5,      4,     40),
    "SAM_05": (54,     3,      5,      5,     36),
    "SAM_06": (55,     3,      5,      6,     38),
    "SAM_07": (56,     3,      5,      7,     9),
    "HOS_00": (57,     3,      6,      0,     62),
    "HOS_01": (58,     3,      6,      1,     28),
    "HOS_02": (59,     3,      6,      2,     54),
    "HOS_03": (60,     3,      6,      3,     60),
    "HOS_04": (61,     3,      6,      4,     14),
    "HOS_05": (62,     3,      6,      5,     61),
    "HOS_06": (63,     3,      6,      6,     55),
    "HOS_07": (64,     3,      6,      7,     63),

}
