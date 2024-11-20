# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_movecosts.py
# modified to work with MoveList.py instead of the db
"""
This module is used for modifying BP costs of badges, FP costs of both badge
and partner moves and SP costs for star power moves.
"""

from ..data.enum_options import RandomMoveCosts
from ..data.MoveList import move_table

value_limits = {
    "BADGE":     {"BP": {"min": 1, "max": 8, }, "FP": {"min": 1, "max": 7, }},
    "PARTNER":   {"FP": {"min": 1, "max": 8, }},
    "STARPOWER": {"FP": {"min": 1, "max": 3, }}
}


# gets the data address? for a move, from https://github.com/icebound777/PMR-SeedGenerator/blob/main/db/move.py
def get_key(data):
    return (0xA6 << 24) | (data[4] << 16) | (data[5] << 8) | data[6]


def _get_shuffled_costs(movetype, costtype, random):
    """
    Returns a list of tuples where the first value holds the dbkey for a move
    cost and the second value holds the shuffled cost depending on which
    move type and cost type are given as parameters.
    """
    shuffled_costs = []
    db_keys = []
    db_values = []

    for id, data in move_table.items():
        if data[1] == movetype and data[2] == costtype:
            db_keys.append(get_key(data))
            db_values.append(data[3])

    random.shuffle(db_values)

    for db_key, db_value in zip(db_keys, db_values):
        shuffled_costs.append((db_key, db_value))

    return shuffled_costs


def _get_balanced_random_costs(movetype: str, costtype: str, random) -> list:
    """
    Returns a list of tuples where the first value holds the dbkey for a badge
    BP cost and the second value holds its randomized BP cost.
    """
    random_costs = []

    min_value = value_limits.get(movetype).get(costtype).get("min")
    max_value = value_limits.get(movetype).get(costtype).get("max")

    for id, data in move_table.items():
        if data[1] == movetype and data[2] == costtype:
            default_cost = data[3]

            # 10% Chance to pick randomly between 1 and 8, else randomly choose
            # from -2 to +2, clamping to 1-8
            if random.randint(1, 10) == 10:
                new_cost = random.randint(min_value, max_value)
            else:
                if movetype == "STARPOWER":
                    new_cost = default_cost + random.choice([-1, 0, 1])
                else:
                    new_cost = default_cost + random.choice([-2, -1, 0, 1, 2])

                if new_cost < min_value:
                    new_cost = min_value
                if new_cost > max_value:
                    # Flower Fanatic is the only badge allowed to scale to 9
                    # since it's the only badge with that high of a basic cost
                    if data[0] == "FlowerFanatic":
                        new_cost = 9
                    else:
                        new_cost = max_value

            random_costs.append((get_key(data), new_cost))

    return random_costs


def _get_fully_random_costs(movetype: str, costtype: str, random) -> list:
    """
    Returns a list of tuples where the first value holds the dbkey for a cost
    and the second value holds its fully randomized cost value.
    """
    fully_random_costs = []

    min_value = value_limits.get(movetype).get(costtype).get("min")
    if (movetype, costtype) == ("BADGE", "BP"):
        # Special case for bp costs: 1-8 simply has too high of a median
        max_value = 6
    else:
        max_value = value_limits.get(movetype).get(costtype).get("max")

    for id, data in move_table.items():
        if data[1] == movetype and data[2] == costtype:
            new_cost = random.randint(min_value, max_value)
            fully_random_costs.append((get_key(data), new_cost))
            # print(f"{move.move_name}: {move.cost_value} -> {new_cost}")

    return fully_random_costs


def get_randomized_moves(
    badges_bp_setting: int,
    badges_fp_setting: int,
    partner_fp_setting: int,
    starpower_setting: int,
    random
):
    """
    Returns a list of tuples where the first value holds the dbkey for a move
    cost and the second value holds the shuffled FP,BP,SP cost.
    """
    rnd_cost_functions = {
        RandomMoveCosts.BALANCED_RANDOM: _get_balanced_random_costs,
        RandomMoveCosts.SHUFFLED: _get_shuffled_costs,
        RandomMoveCosts.FULLY_RANDOM: _get_fully_random_costs,
    }

    move_costs = []

    if badges_bp_setting in rnd_cost_functions:
        new_cost = rnd_cost_functions.get(badges_bp_setting)("BADGE", "BP", random)
        move_costs.extend(new_cost)

    if badges_fp_setting in rnd_cost_functions:
        new_cost = rnd_cost_functions.get(badges_fp_setting)("BADGE", "FP", random)
        move_costs.extend(new_cost)

    if partner_fp_setting in rnd_cost_functions:
        new_cost = rnd_cost_functions.get(partner_fp_setting)("PARTNER", "FP", random)
        move_costs.extend(new_cost)

    if starpower_setting in rnd_cost_functions:
        new_cost = rnd_cost_functions.get(starpower_setting)("STARPOWER", "FP", random)
        move_costs.extend(new_cost)

    return move_costs
