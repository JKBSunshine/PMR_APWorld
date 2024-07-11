import math
import random
from copy import deepcopy

from ..data.enum_options import IncludeFavorsMode, RandomizeConsumablesMode
from ..data.item_exclusion import exclude_due_to_settings
from ..data.item_scores import item_scores
from ..data.itemlocation_special import kootfavors_reward_locations, kootfavors_keyitem_locations, limited_by_item_areas

from BaseClasses import Item
from ..data.LocationsList import location_table, location_groups
from ..data.ItemList import item_table, item_groups


def _get_random_consumables(n: int, available_items: list) -> list:
    """
    Returns a list of n items, with categories similar to vanilla distribution
    """
    weights = {
        "battle": 50,
        "heal": 45,
        "taycet": 5,
    }
    item_weights = [weights[item["type"]] for item in available_items]

    return random.choices(available_items, item_weights, k=n)


def _balance_consumables(items: list, available_items: list, target_score: int):
    """
    Modifies a list of consumables until its score is close enough to the target score
    """
    new_items = items.copy()
    pool_score = sum([item["score"] for item in new_items])

    lowest_item = item_scores[0]
    lowest_score = lowest_item["score"]
    highest_item = item_scores[len(item_scores) - 1]
    highest_score = highest_item["score"]
    score_diff = math.ceil((highest_score - lowest_score) / 2)

    # Randomly adjust the items to bring closer to target score
    while pool_score < target_score - score_diff or pool_score > target_score + score_diff:
        if pool_score < target_score:
            # Upgrade an item
            item_weights = [highest_score - item["score"] for item in new_items]
            i = random.choices([i for i in range(len(new_items))], item_weights).pop()
            old_item = new_items[i]
            legal_items = [item for item in available_items if
                           item["score"] > old_item["score"] and item["type"] == old_item["type"]]
        else:
            # Downgrade an item
            item_weights = [item["score"] - lowest_score for item in new_items]
            i = random.choices([i for i in range(len(new_items))], item_weights).pop()
            old_item = new_items[i]
            legal_items = [item for item in available_items if
                           item["score"] < old_item["score"] and item["type"] == old_item["type"]]

        # If there's no legal items to upgrade/downgrade to, try again
        if len(legal_items) == 0:
            continue

        new_item = random.choice(legal_items)
        pool_score += new_item["score"] - old_item["score"]
        new_items[i] = new_item

    return new_items


def get_randomized_itempool(itempool: list, consumable_mode: int, quality: int, add_unused_items: bool) -> list:
    """
    Returns a randomized general item pool according to consumable mode
    Balanced random mode creates an item pool that has a value equal
    to the input pool's value, multiplied by the quality percentage
    """
    # Consumable mode:
    # 0: vanilla (no quality)
    # 1: full random (no quality)
    # 2: balanced random (quality applies)
    # 3: mystery only (no quality)

    # vanilla
    if consumable_mode == RandomizeConsumablesMode.OFF:
        return itempool

    def is_consumable(item_name):
        item_score_obj = next((x for x in item_scores if x.get("name") == item_name), None)
        return item_score_obj is not None

    new_items = []
    kept_items = [x for x in itempool if not is_consumable(x)]
    removed_items = [x for x in itempool if is_consumable(x)]
    target_count = len(removed_items)

    # Random or Balanced Random
    if (consumable_mode == RandomizeConsumablesMode.FULL_RANDOM
            or consumable_mode == RandomizeConsumablesMode.BALANCED_RANDOM):

        if add_unused_items:
            available_items = item_scores
        else:
            available_items = [
                item for item in item_scores if item["name"] not in ["Hustle Drink", "Insecticide Herb"]
            ]

        # Generate fully random pool
        new_items = _get_random_consumables(target_count, available_items)

        # Balance according to quality factor
        if consumable_mode == RandomizeConsumablesMode.BALANCED_RANDOM:
            target_score = 0
            for item_name in removed_items:
                target_score += next(item["score"] for item in item_scores if item["name"] == item_name)

            # Multiply score by the quality factor
            target_score = math.floor(target_score * (quality / 100))
            new_items = _balance_consumables(new_items, available_items, target_score)

        # Convert from scored dict entries to proper item_obj list
        new_items = [item["name"] for item in new_items]

    # Mystery only
    elif consumable_mode == RandomizeConsumablesMode.MYSTERY_ONLY:
        mystery_item = "Mystery"
        for _ in range(target_count):
            new_items.append(deepcopy(mystery_item))

    new_itempool = kept_items + new_items
    assert (len(itempool) == len(new_itempool))
    return new_itempool


def get_trapped_itempool(itempool: list,
                         trap_mode: int,
                         randomize_favors_mode: int,
                         do_randomize_dojo: bool,
                         keyitems_outside_dungeon: bool,
                         power_star_hunt: bool,
                         add_beta_items: bool,
                         do_partner_upgrade_shuffle: bool) -> list:
    """
    Modifies and returns a given item pool after placing trap items.
    This swaps out consumable items with trap items, which do not actually give
    the item to Mario, and instead damage him and make him drop coins.
    The items need not necessarily look like consumables, and can use the
    sprites of badges, key items and others instead.
    """
    # Trap mode:
    # 0: no traps
    # 1: sparse
    # 2: moderate
    # 3: plenty

    if trap_mode == 0:
        return itempool

    if trap_mode == 1:
        max_traps = 15
    elif trap_mode == 2:
        max_traps = 35
    else:
        max_traps = 80

    koot_items = {"rewards": [], "keyitems": []}
    for name, data in location_table.items():
        if data[0] in kootfavors_reward_locations:
            koot_items["rewards"].append(data[5])
        if data[0] in kootfavors_keyitem_locations:
            koot_items["keyitems"].append(data[5])

    trap_flag = 0x2000
    new_itempool = []
    fakeable_items = []
    dungeon_items = []
    for name, data in item_table.items():
        if name in ["KEYITEM", "PARTNER", "BADGE", "GEAR"]:
            if (data[4] and not add_beta_items) or data[6]:
                continue
            if (not do_randomize_dojo
                    and name in exclude_due_to_settings.get("do_randomize_dojo")):
                continue
            if (randomize_favors_mode < IncludeFavorsMode.RND_REWARD_VANILLA_KEYITEMS
                    and name in koot_items["rewards"]):
                continue
            if (randomize_favors_mode < IncludeFavorsMode.FULL_SHUFFLE
                    and name in koot_items["keyitems"]):
                continue
            if not keyitems_outside_dungeon:
                # If no wild keys then don't use them for traps
                if not dungeon_items:
                    for area_key_dict in limited_by_item_areas.values():
                        for key_list in area_key_dict.values():
                            dungeon_items.extend(key_list)
                if name in dungeon_items:
                    continue

            fakeable_items.append(name)

    # Add Power Star traps if necessary
    if power_star_hunt:
        fakeable_items.append("PowerStar7F")

    # Bias towards placing UltraStone or upgrade traps, as requested by clover
    if do_partner_upgrade_shuffle:
        for item in (item_groups["PartnerUpgrade"]):
            fakeable_items.append(item)
    else:
        for x in range(0, 9):
            fakeable_items.extend("Ultra Stone")

    cnt_traps = 0
    shuffled_pool = itempool.copy()
    random.shuffle(shuffled_pool)

    for item in shuffled_pool:
        if item.item_type != "ITEM" or cnt_traps >= max_traps:
            new_itempool.append(item)
        else:
            new_trapitem = random.choice(fakeable_items)
            new_trapitem.value = new_trapitem.value | trap_flag
            new_itempool.append(new_trapitem)
            cnt_traps += 1

    return new_itempool
