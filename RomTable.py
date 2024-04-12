# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/table.py

from .data.RomOptionList import rom_option_table, ap_to_rom_option_table
from .modules.random_blocks import get_block_key
from .options import (EnemyDamage, PaperMarioOptions, PartnerUpgradeShuffle, ShuffleKootFavors, ShuffleLetters,
                      BowserCastleMode)
from .data.MysteryOptions import MysteryOptions
from .data.starting_maps import starting_maps
from .data.node import Node
from .items import PMItem
from .data.ItemList import item_groups, item_multiples_ids


class RomTable:
    instance = None
    default_db = {}
    db = {}
    info = {}

    def __init__(self):
        if RomTable.instance is None:
            RomTable.instance = self
        else:
            self = RomTable.instance

    def __getitem__(self, key):
        return self.db[key]

    def generate_pairs(self,  options: PaperMarioOptions, placed_items: list[Node], placed_blocks: dict, entrances: list,
                       actor_attributes: list, move_costs: list, palettes: list, quizzes: list,
                       music_list: list, mapmirror_list: list, puzzle_list: list, mystery_opts: MysteryOptions):
        table_data = []

        # Options
        option_dbtuples = get_dbtuples(options, mystery_opts)

        for option_data in option_dbtuples:
            option_key = option_data[0]
            option_value = option_data[1]
            if isinstance(option_value, int) and option_value < 0:
                option_value = 0x100000000 + option_value
            table_data.append({
                "key": option_key,
                "value": option_value,
            })

        # temp fix for multiworld
        table_data.append({
            "key": 0xAF050000,
            "value": 0x00000000
        })

        # Quizzes
        for key, value in quizzes:
            table_data.append({
                "key": key,
                "value": value
            })

        # Items
        repeat_items = {}
        for node in placed_items:
            if node.key_name_item is not None and node.current_item is not None:
                item_id = node.current_item.id
                # Progressive items default to their highest ids for in-game placement
                # When received, we receive the lowest IDs
                if item_id in item_multiples_ids.keys():
                    if item_id not in repeat_items.keys():
                        repeat_items[item_id] = len(item_multiples_ids[item_id]) - 1

                    item_id = item_multiples_ids[item_id][repeat_items[item_id]]
                    repeat_items[node.current_item.id] -= 1

                table_data.append({
                    "key": node.get_item_key(),
                    "value": item_id,
                })

            # Item Prices
            if (node.key_name_price is not None
                and (node.key_name_price.startswith("ShopPrice")
                     or node.key_name_price.startswith("RewardAmount"))):
                table_data.append({
                    "key": node.get_price_key(),
                    "value": node.current_item.base_price
                })

        for name, value in placed_blocks.items():
            table_data.append({
                "key": get_block_key(name),
                "value": value
            })

        # Entrances
        for key, value in entrances:
            table_data.append({
                "key": key,
                "value": value
            })

        # Actor Attributes
        for key, value in actor_attributes:
            table_data.append({
                "key": key,
                "value": value
            })

        # Palettes
        for key, value in palettes:
            table_data.append({
                "key": key,
                "value": value
            })

        # Move Costs
        for key, value in move_costs:
            table_data.append({
                "key": key,
                "value": value
            })

        # Audio
        for key, value in music_list:
            table_data.append({
                "key": key,
                "value": value
            })

        # Map mirroring
        for key, value in mapmirror_list:
            table_data.append({
                "key": key,
                "value": value
            })

        # Puzzles & Minigames
        for key, value in puzzle_list:
            table_data.append({
                "key": key,
                "value": value
            })

        table_data.sort(key=lambda pair: pair["key"])
        return table_data

    def create(self):
        self.info = get_table_info()


def get_table_info():
    # Defaults
    table_info = {
        "magic_value": 0x504D4442,
        "header_size": 0x20,
        "db_size": 0,
        "seed": 0xDEADBEEF,
        "address": 0x1D00000,
        "formations_offset": 0,
        "itemhints_offset": 0,
        "auth_address": 0x1cffff0
    }

    return table_info


def generate_table_pairs(value_set):
    table_data = []

    for key, value in value_set:
        table_data.append({
            "key": key,
            "value": value
        })

    table_data.sort(key=lambda pair: pair["key"])
    return table_data


def get_dbtuples(options: PaperMarioOptions, mystery_opts: MysteryOptions) -> list:
    dbtuples = []

    # map tracker check and shop bits
    map_tracker_bits = 0x1 + 0x2
    if options.shuffle_hidden_panels.value:
        map_tracker_bits += 0x4
    if options.partner_upgrades.value >= PartnerUpgradeShuffle.option_Super_Block_Locations:
        map_tracker_bits += 0x8
    if options.overworld_coins.value:
        map_tracker_bits += 0x10
    if options.coin_blocks.value:
        map_tracker_bits += 0x20
    if options.koot_coins.value:
        map_tracker_bits += 0x40
    if options.foliage_coins.value:
        map_tracker_bits += 0x80
    if options.dojo.value:
        map_tracker_bits += 0x100
    if options.koot_favors.value != ShuffleKootFavors.option_Vanilla:
        map_tracker_bits += 0x200
    if options.trading_events.value:
        map_tracker_bits += 0x400
    if options.letter_rewards.value != ShuffleLetters.option_Vanilla:
        map_tracker_bits += 0x800
    if not options.open_forest.value:
        map_tracker_bits += 0x1000
    if options.bowser_castle_mode.value == BowserCastleMode.option_Vanilla:
        map_tracker_bits += 0x2000
    if options.bowser_castle_mode.value <= BowserCastleMode.option_Shortened:
        map_tracker_bits += 0x4000
    if (options.partner_upgrades.value >= PartnerUpgradeShuffle.option_Super_Block_Locations
            and options.super_multi_blocks.value):
        map_tracker_bits += 0x8000

    map_tracker_check_bits = map_tracker_bits
    map_tracker_shop_bits = 0x7
    if options.bowser_castle_mode.value <= BowserCastleMode.option_Shortened:
        map_tracker_shop_bits += 0x8

    # status menu palette bits
    menu_color_a, menu_color_b = 0xEBE677FF, 0x8E5A25FF
    match options.status_menu_palette.value:
        case 0:
            menu_color_a, menu_color_b = 0xEBE677FF, 0x8E5A25FF
        case 1:
            menu_color_a, menu_color_b = 0x8D8FFFFF, 0x2B4566FF
        case 2:
            menu_color_a, menu_color_b = 0xAAD080FF, 0x477B53FF
        case 3:
            menu_color_a, menu_color_b = 0x8ED4ECFF, 0x436245FF
        case 4:
            menu_color_a, menu_color_b = 0xD7BF74FF, 0x844632FF
        case 5:
            menu_color_a, menu_color_b = 0xB797B7FF, 0x62379AFF
        case 6:
            menu_color_a, menu_color_b = 0xC0C0C0FF, 0x404040FF

    for rom_option, ap_option in ap_to_rom_option_table.items():
        option_key = get_db_key(rom_option)
        option_value = -1
        if ap_option == "":
            #  handle options that are calculated, not yet implemented, or otherwise not changeable by the player
            match rom_option:
                # Always turned on
                case "BlocksMatchContent" | "FastTextSkip" | "ShuffleItems" | "RandomQuiz" \
                     | "PeachCastleReturnPipe" | "MultiworldEnabled":
                    option_value = 1
                # Always turned off
                case "ChallengeMode" | "ShuffleDungeonRooms" | "ShuffleEntrancesByAll" | "MatchEntranceTypes" \
                     | "Widescreen" | "PawnsEnabled":
                    option_value = 0
                # NYI, giving dungeon keys temporarily until that logic is fixed
                case "StartingItem0" | "StartingItem1" | "StartingItem2" | "StartingItem3" | "StartingItem4":
                    option_value = 0
                case "StartingItem5" | "StartingItem6" | "StartingItem7" | "StartingItem8" | "StartingItem9":
                    option_value = 0
                case "StartingItemA" | "StartingItemB" | "StartingItemC" | "StartingItemD" | "StartingItemE":
                    option_value = 0
                case "StartingItemF":
                    option_value = 0
                case "XPMultiplier":
                    option_value = int(options.enemy_xp_multiplier.value)
                # One setting on the front end, but two separate flags for the mod
                case "DoubleDamage":
                    option_value = options.enemy_damage.value == EnemyDamage.option_Double_Pain
                case "QuadrupleDamage":
                    option_value = options.enemy_damage.value == EnemyDamage.option_Quadruple_Pain
                case "EnabledCheckBits":
                    option_value = map_tracker_check_bits
                case "EnabledShopBits":
                    option_value = map_tracker_shop_bits
                case "Box5ColorA":
                    option_value = menu_color_a
                case "Box5ColorB":
                    option_value = menu_color_b
                case "ItemChoiceA":
                    option_value = mystery_opts.mystery_itemA
                case "ItemChoiceB":
                    option_value = mystery_opts.mystery_itemB
                case "ItemChoiceC":
                    option_value = mystery_opts.mystery_itemC
                case "ItemChoiceD":
                    option_value = mystery_opts.mystery_itemD
                case "ItemChoiceE":
                    option_value = mystery_opts.mystery_itemE
                case "ItemChoiceF":
                    option_value = mystery_opts.mystery_itemF
                case "ItemChoiceG":
                    option_value = mystery_opts.mystery_itemG
                # Calculated based on starting stats
                case "StartingLevel":
                    option_value = int(options.starting_hp.value / 5 +
                                       options.starting_fp.value / 5 +
                                       options.starting_bp.value / 3) - 3
                case "StartingMap":
                    option_value = starting_maps[options.starting_map.value][0]

        else:
            option_value = getattr(options, ap_option).value

        dbtuples.append((option_key, option_value))
        # print(f"{rom_option}, {option_value}")
    return dbtuples


def get_db_key(rom_option):
    data = rom_option_table[rom_option]
    return (0xAF << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
