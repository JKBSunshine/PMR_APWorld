# not entirely, but partially from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/logic.py
# follows examples in OoT's implementation

from collections import namedtuple
from itertools import chain

from .data.chapter_logic import get_bowser_castle_removed_locations, areas_by_chapter
from .data.ItemList import taycet_items, item_table, progression_miscitems, item_groups, item_multiples_base_name
from .data.LocationsList import location_groups, location_table, missable_locations
from .options import *
from .data.item_exclusion import exclude_due_to_settings, exclude_from_taycet_placement
from .modules.modify_itempool import get_trapped_itempool, get_randomized_itempool
from BaseClasses import ItemClassification as Ic, LocationProgressType
from .data.enum_types import BlockType
from .Locations import location_factory
from .data.chapter_logic import get_chapter_excluded_item_names, get_chapter_excluded_location_names

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import PaperMarioWorld


def generate_itempool(pm_world):
    world = pm_world.multiworld
    player = pm_world.player

    (pool, placed_items, placed_items_excluded) = get_pool_core(pm_world)

    pm_world.itempool = [pm_world.create_item(item) for item in pool]
    for (location_name, item) in placed_items.items():
        location = world.get_location(location_name, player)
        location.place_locked_item(pm_world.create_item(item, allow_arbitrary_name=True))

    for (location_name, item) in placed_items_excluded.items():
        location = location_factory(location_name, player)
        location.place_locked_item(pm_world.create_item(item, allow_arbitrary_name=True))
        pm_world.ch_excluded_locations.append(location)


def get_pool_core(world: "PaperMarioWorld"):

    pool_misc_progression_items = []
    pool_other_items = []
    pool_progression_items = []
    pool_coins_only = []
    pool_illogical_consumables = []
    pool_badges = []
    pool = []

    placed_items = {}

    bc_removed_locations = get_bowser_castle_removed_locations(world.options.bowser_castle_mode.value)

    # items and locations excluded from chapters for LCL get handled differently from normal excluded locations
    ch_excluded_locations = []
    ch_excluded_items = []
    placed_items_excluded = {}

    if world.options.limit_chapter_logic.value:
        ch_excluded_locations = get_chapter_excluded_location_names(world.excluded_spirits,
                                                                    world.options.letter_rewards.value)
        ch_excluded_items = get_chapter_excluded_item_names(world.excluded_spirits)

    # Exclude locations that are either missable or are going to be considered not in logic based on settings
    excluded_locations = missable_locations + get_locations_to_exclude(world, bc_removed_locations)

    # remove unused items from the pool

    for loc_name in location_table:

        if loc_name not in ch_excluded_locations and loc_name not in bc_removed_locations:
            location = world.get_location(loc_name)
        else:
            location = location_factory(loc_name, world.player)

        if location.vanilla_item is None:
            continue

        item = location.vanilla_item
        itemdata = item_table[item]
        shuffle_item = True

        # Excluded locations
        if location.name in excluded_locations:
            location.progress_type = LocationProgressType.EXCLUDED

        # Sometimes placed items

        if location.name in location_groups["OverworldCoin"]:
            shuffle_item = world.options.overworld_coins.value
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["BlockCoin"]:
            shuffle_item = world.options.coin_blocks.value
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["FoliageCoin"]:
            shuffle_item = world.options.foliage_coins.value
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["ShopItem"]:
            shuffle_item = world.options.include_shops.value
            if not shuffle_item:
                location.disabled = True

        if location.name in location_groups["HiddenPanel"]:
            shuffle_item = world.options.shuffle_hidden_panels.value
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["FavorReward"]:
            # coins get shuffled only if other rewards are also shuffled
            if location.name in location_groups["FavorCoin"]:
                shuffle_item = (world.options.koot_coins.value and
                                (world.options.koot_favors.value != ShuffleKootFavors.option_Vanilla))
            else:
                shuffle_item = (world.options.koot_favors.value != ShuffleKootFavors.option_Vanilla)

            if not shuffle_item:
                location.disabled = True

        if location.name in location_groups["FavorItem"]:
            shuffle_item = (world.options.koot_favors.value == ShuffleKootFavors.option_Full_Shuffle)
            if not shuffle_item:
                location.disabled = True

        if location.name in location_groups["LetterReward"]:
            if location.name == "GR Goomba Village Goompapa Letter Reward 2":
                shuffle_item = (world.options.letter_rewards.value in [ShuffleLetters.option_Final_Letter_Chain_Reward,
                                                                       ShuffleLetters.option_Full_Shuffle])
            elif location.name in location_groups["LetterChain"]:
                shuffle_item = (world.options.letter_rewards.value == ShuffleLetters.option_Full_Shuffle)

            else:
                shuffle_item = (world.options.letter_rewards.value != ShuffleLetters.option_Vanilla)

            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["RadioTradeEvent"]:
            shuffle_item = world.options.trading_events.value
            if not shuffle_item:
                location.disabled = True

        if location.name in location_groups["DojoReward"]:
            shuffle_item = world.options.dojo.value
            if not shuffle_item:
                location.disabled = True

        if location.vanilla_item == "Forest Pass":
            shuffle_item = (not world.options.open_forest.value)
            if not shuffle_item:
                location.disabled = True

        if location.name in location_groups["Partner"]:
            shuffle_item = world.options.partners.value
            if not shuffle_item:
                location.disabled = True

        if location.name in location_groups["Gear"]:
            # hammer 1 bush is special in that it is made to not be empty even if starting with hammer
            if location.name == "GR Jr. Troopa's Playground In Hammer Bush":
                shuffle_item = ((world.options.gear_shuffle_mode.value != GearShuffleMode.option_Vanilla) or
                                (world.options.starting_hammer.value == StartingHammer.option_Hammerless))
            else:
                shuffle_item = (world.options.gear_shuffle_mode.value != GearShuffleMode.option_Vanilla)
            if not shuffle_item:
                location.disabled = True

        if location.name in location_groups["RandomBlock"]:
            shuffle_item = world.placed_blocks[location.name] == BlockType.YELLOW

            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.identifier in ["DRO_01/ShopItemB", "DRO_01/ShopItemD", "DRO_01/ShopItemE"]:
            shuffle_item = world.options.random_puzzles.value

            if not shuffle_item:
                location.disabled = True

        if location.name in ch_excluded_locations and item in ch_excluded_items:
            shuffle_item = not world.options.limit_chapter_logic.value

        # add it to the proper pool, or place the item
        if shuffle_item:

            # hammer bush gets shuffled as a Tayce T item if shuffling gear locations and not hammerless
            if (location.name == "GR Jr. Troopa's Playground In Hammer Bush" and
                    (world.options.gear_shuffle_mode.value == GearShuffleMode.option_Gear_Location_Shuffle) and
                    (world.options.starting_hammer.value != StartingHammer.option_Hammerless)):
                pool_progression_items.append(world.random.choice([x for x in taycet_items
                                                                   if x not in exclude_from_taycet_placement]))


            # some progression items need to be in replenishable locations, we only need one of each
            elif item in progression_miscitems:
                if item not in pool_misc_progression_items:
                    pool_misc_progression_items.append(item)
                else:
                    pool_illogical_consumables.append(item)

            # progression items are shuffled; include gear and star pieces from rip cheato
            elif (itemdata[1] == Ic.progression or
                  (location.name in location_groups["ShopItem"] and
                   world.options.include_shops.value and "Star Piece" in item)) and item not in ch_excluded_items:
                pool_progression_items.append(item)

            # split other items into their own pools; these other pools get modified before being sent elsewhere
            elif itemdata[0] == "COIN":
                pool_coins_only.append(item)
            elif itemdata[0] == "ITEM":
                pool_illogical_consumables.append(item)
            elif itemdata[0] == "BADGE":
                pool_badges.append(item)
            else:
                pool_other_items.append(item)
        elif location.name in ch_excluded_locations:
            # keep out of logic placed items separate, remove the location and item from remaining excluded lists
            placed_items_excluded[location.name] = item
            ch_excluded_locations.remove(location.name)

            # below only applies to key items in the chapter
            if item in ch_excluded_items:
                ch_excluded_items.remove(item)
        else:
            placed_items[location.name] = item

    # end of location for loop

    # at this point every location's item should be either left unshuffled or added to a pool
    # we want to modify these pools according to settings and make sure to have the right number of items

    target_itempool_size = (
            len(pool_progression_items)
            + len(pool_misc_progression_items)
            + len(pool_coins_only)
            + len(pool_illogical_consumables)
            + len(pool_badges)
            + len(pool_other_items)
            - len(bc_removed_locations)
    )

    # add power stars
    if world.options.power_star_hunt.value and world.options.total_power_stars.value > 0:
        for i in range(0, world.options.total_power_stars.value):
            pool_progression_items.append("Power Star")

    # add 5 item pouches
    if world.options.item_pouches.value:
        for i in range(0, 5):
            pool_other_items.append("Pouch Upgrade")

    # add beta items
    if world.options.beta_items.value:
        pool_other_items.extend(item_groups["ItemBeta"])
        for badge in item_groups["BadgeBeta"]:
            pool_badges.append(get_item_multiples_base_name(badge))

    # add unused badge dupes
    if world.options.unused_badge_dupes.value:
        for badge in item_groups["BadgeDupe"]:
            if not (world.options.beta_items.value and badge in item_groups["BadgeBeta"]):
                pool_badges.append(get_item_multiples_base_name(badge))

    # add progressive badges
    if world.options.progressive_badges.value:
        # 3 copies of each progressive badge
        for name in item_groups["ProgBadge"]:
            for i in range(0, 3):
                pool_badges.append(name)

    # add normal boots
    if world.options.starting_boots.value == StartingBoots.option_Jumpless:
        pool_progression_items.append("Progressive Boots")

    # add two of each partner upgrade item, taking care not to add unplaceable ones (goompa upgrades)
    if world.options.partner_upgrades.value != PartnerUpgradeShuffle.option_Vanilla:
        for i in range(0, 2):
            pool_other_items.extend(item_groups["PartnerUpgrade"])

    # adjust item pools based on settings
    items_to_remove_from_pools = get_items_to_exclude(world)

    while items_to_remove_from_pools:
        item = items_to_remove_from_pools.pop()
        if item in pool_progression_items:
            pool_progression_items.remove(item)
            continue
        if item in pool_misc_progression_items:
            pool_misc_progression_items.remove(item)
            continue
        if item in pool_badges:
            pool_badges.remove(item)
            continue
        if item in pool_other_items:
            pool_other_items.remove(item)
            continue

    # If we have set a badge pool limit and exceed that, remove random badges
    # until that condition is satisfied
    if len(pool_badges) > world.options.badge_pool_limit.value:
        world.random.shuffle(pool_badges)
        while len(pool_badges) > world.options.badge_pool_limit.value:
            pool_badges.pop()

    # If the item pool is the wrong size now, fix it by filling up or clearing out items
    cur_itempool_size = (
            len(pool_progression_items)
            + len(pool_misc_progression_items)
            + len(pool_coins_only)
            + len(pool_illogical_consumables)
            + len(pool_badges)
            + len(pool_other_items)
    )

    # add random tayce t items if we need to add items for some reason
    while target_itempool_size > cur_itempool_size:
        pool_illogical_consumables.append(world.random.choice([x for x in taycet_items
                                                               if x not in exclude_from_taycet_placement]))
        cur_itempool_size += 1

    # remove coins first, then consumables if we need to keep going
    if target_itempool_size < cur_itempool_size:
        world.random.shuffle(pool_illogical_consumables)
        while target_itempool_size < cur_itempool_size:
            if len(pool_coins_only) > 20:
                trashable_items = pool_coins_only
            else:
                trashable_items = pool_illogical_consumables
            trashable_items.pop()
            cur_itempool_size -= 1

    # Re-join the non-required items into one array
    pool_other_items.extend(pool_coins_only)
    pool_other_items.extend(pool_illogical_consumables)
    pool_other_items.extend(pool_badges)

    # Randomize consumables if needed
    pool_other_items = get_randomized_itempool(
        pool_other_items,
        world.options.consumable_item_pool.value,
        world.options.consumable_item_quality.value,
        world.options.beta_items.value
    )

    # before adding traps, fill up the out of logic locations with items that aren't progression
    # wouldn't want traps to not make it into the multiworld pool, would we?
    if world.options.limit_chapter_logic.value:
        world.random.shuffle(ch_excluded_locations)

        # shuffle items but then sort to put useful items in the front so that filler items go to out of logic locations first
        world.random.shuffle(pool_other_items)
        pool_other_items.sort(key=lambda item: 1 if item_table[item][1] == Ic.filler else 0)

        # save some filler items for the excluded locations; not the chapter ones, but from get_locations_to_exclude
        for _ in excluded_locations:
            pool.append(pool_other_items.pop())

        for loc in ch_excluded_locations:
            placed_items_excluded[loc] = pool_other_items.pop()

    # add traps
    pool_other_items = get_trapped_itempool(
        pool_other_items,
        world.options.item_traps.value,
        world.options.koot_favors.value,
        world.options.dojo.value,
        world.options.keysanity.value,
        (world.options.power_star_hunt.value and world.options.total_power_stars.value > 0),
        world.options.beta_items.value,
        world.options.partner_upgrades.value
    )

    # now we have the full pool

    pool.extend(pool_progression_items)
    pool.extend(pool_other_items)
    pool.extend(pool_misc_progression_items)

    return pool, placed_items, placed_items_excluded


def get_items_to_exclude(world: "PaperMarioWorld") -> list:
    """
    Returns a list of items that should not be placed or given to Mario at the
    start.
    """
    excluded_items = []

    if world.options.dojo.value:
        for item_name in exclude_due_to_settings.get("do_randomize_dojo"):
            excluded_items.append(item_name)

    if world.options.start_with_goombario.value:
        excluded_items.append("Goombario")
    if world.options.start_with_kooper.value:
        excluded_items.append("Kooper")
    if world.options.start_with_bombette.value:
        excluded_items.append("Bombette")
    if world.options.start_with_parakarry.value:
        excluded_items.append("Parakarry")
    if world.options.start_with_bow.value:
        excluded_items.append("Bow")
    if world.options.start_with_watt.value:
        excluded_items.append("Watt")
    if world.options.start_with_sushie.value:
        excluded_items.append("Sushie")
    if world.options.start_with_lakilester.value:
        excluded_items.append("Lakilester")

    if world.options.open_blue_house.value:
        for item_name in exclude_due_to_settings.get("startwith_bluehouse_open"):
            excluded_items.append(item_name)

    if world.options.open_forest.value:
        for item_name in exclude_due_to_settings.get("startwith_forest_open"):
            excluded_items.append(item_name)

    if world.options.magical_seeds.value < 4:
        for item_name in exclude_due_to_settings.get("magical_seeds_required").get(world.options.magical_seeds.value):
            excluded_items.append(item_name)

    if world.options.bowser_castle_mode.value > BowserCastleMode.option_Vanilla:
        for item_name in exclude_due_to_settings.get("shorten_bowsers_castle"):
            excluded_items.append(item_name)
    if world.options.bowser_castle_mode.value == BowserCastleMode.option_Boss_Rush:
        for item_name in exclude_due_to_settings.get("boss_rush"):
            excluded_items.append(item_name)
    if world.options.always_speedy_spin.value:
        for item_name in exclude_due_to_settings.get("always_speedyspin"):
            excluded_items.append(item_name)
    if world.options.always_ispy.value:
        for item_name in exclude_due_to_settings.get("always_ispy"):
            excluded_items.append(item_name)
    if world.options.always_peekaboo.value:
        for item_name in exclude_due_to_settings.get("always_peekaboo"):
            excluded_items.append(item_name)
    if world.options.progressive_badges.value:
        for item_name in exclude_due_to_settings.get("do_progressive_badges"):
            excluded_items.append(item_name)

    if world.options.starting_hammer.value == StartingHammer.option_Ultra:
        excluded_items.append("Progressive Hammer")
    if world.options.starting_hammer.value >= StartingHammer.option_Super:
        excluded_items.append("Progressive Hammer")
    if (world.options.starting_hammer.value >= StartingHammer.option_Normal and
            world.options.gear_shuffle_mode.value != GearShuffleMode.option_Gear_Location_Shuffle):
        excluded_items.append("Progressive Hammer")
    if world.options.starting_boots.value == StartingBoots.option_Ultra:
        excluded_items.append("Progressive Boots")
    if world.options.starting_boots.value >= StartingBoots.option_Super:
        excluded_items.append("Progressive Boots")

    if world.options.partner_upgrades.value:
        for item_name in exclude_due_to_settings.get("partner_upgrade_shuffle"):
            excluded_items.append(item_name)

    return excluded_items


def get_locations_to_exclude(world: "PaperMarioWorld", bc_removed_locations: list) -> list:
    excluded_locations = []

    # exclude locations which require more star spirits than are expected to be needed to beat the seed
    if not world.options.power_star_hunt.value:
        if world.options.star_spirits_required.value < 6:
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 20")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 19")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 18")
        if world.options.star_spirits_required.value < 5:
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 17")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 16")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 15")
            excluded_locations.append("TT Gate District Dojo: Master 3")
            excluded_locations.append("TT Port District Radio Trade Event 3 Reward")
        if world.options.star_spirits_required.value < 4:
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 14")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 13")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 12")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 5 - 3")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 5 - 2")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 5 - 1")
            excluded_locations.append("TT Gate District Dojo: Master 2")
        if world.options.star_spirits_required.value < 3:
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 11")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 10")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 9")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 4 - 3")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 4 - 2")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 4 - 1")
            excluded_locations.append("TT Gate District Dojo: Master 1")
            excluded_locations.append("TT Port District Radio Trade Event 2 Reward")
        if world.options.star_spirits_required.value < 2:
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 8")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 7")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 6")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 3 - 3")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 3 - 2")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 3 - 1")
        if world.options.star_spirits_required.value < 1:
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 5")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 4")
            excluded_locations.append("KR Koopa Village 2 Koopa Koot Reward 3")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 2 - 3")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 2 - 2")
            excluded_locations.append("TT Plaza District Rowf's Shop Set 2 - 1")
            excluded_locations.append("TT Gate District Dojo: Lee")
            excluded_locations.append("TT Port District Radio Trade Event 1 Reward")

    # exclude some amount of chapter 8 locations depending upon access requirements
    late_game_locations = []
    for prefix in areas_by_chapter[8]:
        late_game_locations.extend([name for (name, data) in location_table.items() if name.startswith(prefix)
                                    and name not in bc_removed_locations])
    late_game_locations.append("PCG Hijacked Castle Entrance Hidden Block")
    late_game_locations.append("SSS Star Haven Shop Item 1")
    late_game_locations.append("SSS Star Haven Shop Item 2")
    late_game_locations.append("SSS Star Haven Shop Item 3")
    late_game_locations.append("SSS Star Haven Shop Item 4")
    late_game_locations.append("SSS Star Haven Shop Item 5")
    late_game_locations.append("SSS Star Haven Shop Item 6")

    late_game_exclude_rate = get_star_haven_access_ratio(world.options) * 100

    for location in late_game_locations:
        if world.random.randint(1, 100) <= late_game_exclude_rate:
            excluded_locations.append(location)

    # exclude merlow rewards
    if not world.options.merlow_items.value:
        excluded_locations.extend(location_groups["MerlowReward"])

    # exclude rowf item locations
    if not world.options.rowf_items.value:
        for location in location_groups["RowfShop"]:
            if location not in excluded_locations:
                excluded_locations.append(location)

    # exclude rip cheato locations
    for i in range(0, 11):
        location_name = location_groups["RipCheato"][i]
        if location_table[location_name][5] >= world.options.cheato_items.value:
            excluded_locations.append(location_groups["RipCheato"][i])

    return excluded_locations


def get_item_multiples_base_name(item_name: str) -> str:
    if item_name in item_multiples_base_name.keys():
        return item_multiples_base_name[item_name]
    return item_name


def get_star_haven_access_ratio(options: PaperMarioOptions):
    if options.power_star_hunt.value:
        if options.star_hunt_skips_ch8.value:
            return 1
        else:
            return options.required_power_stars.value / options.total_power_stars.value

    else:
        return options.star_spirits_required.value / 7

