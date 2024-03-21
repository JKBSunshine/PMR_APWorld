# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/table.py

from .data.RomOptionList import rom_option_table, get_key, ap_to_rom_option_table
from .modules.random_quizzes import get_randomized_quizzes
from .options import EnemyDamage
from .data.MysteryOptions import MysteryOptions
from .modules.random_mystery import get_random_mystery

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import PaperMarioWorld


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

    def generate_pairs(self, world: PaperMarioWorld):
        # Get data for options that don't affect logic
        mystery_opts = get_random_mystery(world.options.mystery_shuffle.value)

        table_data = []

        # Set up the option_dbtuples a little differently from upstream to account for different access to settings
        option_dbtuples = []
        for option in ap_to_rom_option_table:
            if option.get("value") == "":
                #  handle options that are calculated, not yet implemented, or otherwise not changeable by the player
                match option.get("key"):
                    case "BlocksMatchContent" | "FastTextSkip" | "ShuffleItems" | "RandomQuiz":
                        option_dbtuples.append({get_key(option.get("key")), 1})
                    case "ChallengeMode" | "ShuffleDungeonRooms" | "ShuffleEntrancesByAll" | "MatchEntranceTypes":
                        option_dbtuples.append({get_key(option.get("key")), 0})
                    case {'id': x} if x.startswith("StartingItem"):
                        option_dbtuples.append({get_key(option.get("key")), 0})
                    case "DoubleDamage":
                        option_dbtuples.append({get_key(option.get("key")),
                                                world.options.enemy_damage.value == EnemyDamage.option_Double_Pain})
                    case "QuadrupleDamage":
                        option_dbtuples.append({get_key(option.get("key")),
                                                world.options.enemy_damage.value == EnemyDamage.option_Quadruple_Pain})
                    case "EnabledCheckBits":
                        option_dbtuples.append({get_key(option.get("key")), 0})  # TODO
                    case "EnabledShopBits":
                        option_dbtuples.append({get_key(option.get("key")), 0})  # TODO
                    case "ItemChoiceA":
                        option_dbtuples.append({get_key(option.get("key")), mystery_opts.mystery_itemA})
                    case "ItemChoiceB":
                        option_dbtuples.append({get_key(option.get("key")), mystery_opts.mystery_itemA})
                    case "ItemChoiceC":
                        option_dbtuples.append({get_key(option.get("key")), mystery_opts.mystery_itemA})
                    case "ItemChoiceD":
                        option_dbtuples.append({get_key(option.get("key")), mystery_opts.mystery_itemA})
                    case "ItemChoiceE":
                        option_dbtuples.append({get_key(option.get("key")), mystery_opts.mystery_itemA})
                    case "ItemChoiceF":
                        option_dbtuples.append({get_key(option.get("key")), mystery_opts.mystery_itemA})
                    case "ItemChoiceG":
                        option_dbtuples.append({get_key(option.get("key")), mystery_opts.mystery_itemA})
                    case "StartingLevel":
                        option_dbtuples.append({get_key(option.get("key")), (world.options.starting_bp.value / 5 +
                                                                             world.options.starting_bp.value / 5 +
                                                                             world.options.starting_bp.value / 3) - 3})
            else:
                option_dbtuples.append({get_key(option.get("key")), getattr(world.options, option.get("value")).value})

        for option_data in option_dbtuples:
            if isinstance(option_data, dict) and "key" in option_data:
                option_data_value = option_data.get("value")
                if isinstance(option_data_value, int) and option_data_value < 0:
                    option_data_value = 0x100000000 + option_data_value
                table_data.append({
                    "key": option_data.get("key"),
                    "value": option_data_value,
                })

        # temp fix for multiworld
        table_data.append({
            "key": 0xAF050000,
            "value": 0x00000000
        })

        # Quizzes
        quizzes = get_randomized_quizzes()

        for key, value in quizzes:
            table_data.append({
                "key": key,
                "value": value
            })

        # Items
        placed_items = world.placed_items
        for node in placed_items:
            if node.key_name_item is not None and node.current_item is not None:
                assert not node.current_item.unplaceable  # sanity check

                table_data.append({
                    "key": node.get_item_key(),
                    "value": node.current_item.value,
                })

            # Item Prices
            if (    node.key_name_price is not None
                and (   node.key_name_price.startswith("ShopPrice")
                     or node.key_name_price.startswith("RewardAmount")
                )
            ):
                table_data.append({
                    "key": node.get_price_key(),
                    "value": node.current_item.base_price
                })

        # Blocks
        placed_blocks = world.placed_blocks
        for key, value in placed_blocks:
            table_data.append({
                "key": key,
                "value": value
            })

        # Entrances
        entrances = []  # world.entrance_list
        for key, value in entrances:
            table_data.append({
                "key": key,
                "value": value
            })

        # Actor Attributes
        actor_attributes = world.enemy_stats
        for key, value in actor_attributes:
            table_data.append({
                "key": key,
                "value": value
            })

        # Palettes
        palettes = world.palette_data
        for key, value in palettes:
            table_data.append({
                "key": key,
                "value": value
            })

        # Move Costs
        move_costs = world.move_costs
        for key, value in move_costs:
            table_data.append({
                "key": key,
                "value": value
            })

        # Audio
        music_list = world.music_list
        for key, value in music_list:
            table_data.append({
                "key": key,
                "value": value
            })

        # Map mirroring
        mapmirror_list = world.static_map_mirroring
        for key, value in mapmirror_list:
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
