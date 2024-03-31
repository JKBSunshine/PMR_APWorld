# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/randomizer.py, pulled functions for rom-related stuff

from typing import TYPE_CHECKING, List, Tuple
import hashlib
import random
from .calculate_crc import recalculate_crcs
from .RomTable import RomTable
from worlds.Files import APContainer
import zipfile
import os
import shutil


from .itemhints import get_itemhints
from .modules.random_actor_stats import get_shuffled_chapter_difficulty
from .modules.random_audio import get_randomized_audio
from .modules.random_formations import get_random_formations
from .modules.random_map_mirroring import get_mirrored_map_list
from .modules.random_movecosts import get_randomized_moves
from .modules.random_palettes import get_randomized_palettes, get_randomized_coinpalette
from .data.MysteryOptions import MysteryOptions
from .modules.random_puzzles_minigames import get_puzzles_minigames
from .modules.random_quizzes import get_randomized_quizzes
from .options import EnemyDifficulty
from .data.ItemList import item_table
from .data.node import Node
from .Locations import PMLocation
from .data.maparea import MapArea
from .modules.random_shop_prices import get_shop_price

class PMContainer(APContainer):
    game: str = 'Paper Mario'

    def __init__(self, patch_data: bytes, base_path: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.zpf_path = base_path + ".zpf"
        container_path = os.path.join(output_directory, base_path + ".appmr")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr(self.zpf_path, self.patch_data)
        super().write_contents(opened_zipfile)


def generate_output(world, output_dir: str) -> None:

    # Set up any options that don't affect logic and thus haven't been set up yet

    # enemy stats
    enemy_stats, chapter_changes = get_shuffled_chapter_difficulty(
        world.options.enemy_difficulty.value, starting_chapter=1)

    battle_formations = []

    if (world.options.formation_shuffle.value or
            world.options.enemy_difficulty.value == EnemyDifficulty.option_Progressive_Scaling):
        battle_formations = get_random_formations(chapter_changes,
                                                  world.options.enemy_difficulty.value ==
                                                  EnemyDifficulty.option_Progressive_Scaling)

    entrance_list = []

    # Coin palette values
    coin_palette_data, coin_palette_targets, coin_palette_crcs = (
        get_randomized_coinpalette(world.options.coin_palette.value))

    # Quizzes are always randomized
    quiz_data = get_randomized_quizzes()

    # No randomizing puzzles for now
    puzzle_list, spoilerlog_puzzles = get_puzzles_minigames(False, world)

    # Default mystery options for now
    mystery_opts = MysteryOptions()


    # Non-coin palettes
    palette_data = get_randomized_palettes(world)

    # Move costs
    move_costs = get_randomized_moves(world.options.badge_bp_shuffle.value,
                                      world.options.badge_fp_shuffle.value,
                                      world.options.partner_fp_shuffle.value,
                                      world.options.sp_shuffle.value)

    # Randomized music
    music_list = get_randomized_audio(world.options.shuffle_music.value,
                                      world.options.shuffle_jingles.value)

    # mirror mode is always off at the moment
    static_map_mirroring = get_mirrored_map_list()

    placed_items = get_filled_node_list(world)
    item_hints = get_itemhints(False, placed_items, world.options)

    write_data_to_rom(target_modfile=world.settings.rom_file,
                      output_directory=output_dir,
                      world=world,
                      placed_items=placed_items,
                      placed_blocks=world.placed_blocks,
                      entrance_list=entrance_list,
                      enemy_stats=enemy_stats,
                      battle_formations=battle_formations,
                      move_costs=move_costs,
                      itemhints=item_hints,
                      coin_palette_data=coin_palette_data,
                      coin_palette_targets=coin_palette_targets,
                      coin_palette_crcs=coin_palette_crcs,
                      palette_data=palette_data,
                      quiz_data=quiz_data,
                      music_list=music_list,
                      mapmirror_list=static_map_mirroring,
                      puzzle_list=puzzle_list,
                      mystery_opts=mystery_opts)

    print("test")


def is_rom_basemod(target_modfile: str) -> bool:
    """
    Checks the md5 hash of a provided target ROM and compares it against the
    version of the base modded Rando ROM that is ascociated with it.
    Returns True if matching.
    """
    basemod_md5_hash = "10785ABD05C36F4C6EEF27A80AE03642"

    hash_md5 = hashlib.md5()
    with open(file=target_modfile, mode="rb") as in_file:
        for chunk in iter(lambda: in_file.read(4096), b""):
            hash_md5.update(chunk)

    # return hash_md5.hexdigest() == basemod_md5_hash
    # I killed this check because currently the randomizer destructively
    # writes to the ROM. It isn't good to remove a safety check, but the
    # CLI is frankly not reasonably usable without this hack in place for now.
    return True


def write_data_to_rom(
    target_modfile: str,
    output_directory: str,
    world,
    placed_items: list,
    placed_blocks: dict,
    entrance_list: list,
    enemy_stats: list,
    battle_formations: list,
    move_costs: list,
    itemhints: list,
    coin_palette_data: list,
    coin_palette_targets: list,
    coin_palette_crcs: list,
    palette_data: list,
    quiz_data: list,
    music_list: list,
    mapmirror_list: list,
    puzzle_list: list,
    mystery_opts: MysteryOptions,
    seed_id=random.randint(0, 0xFFFFFFFF)
):
    """
    Generates key:value pairs of locations and items from a randomized item set
    and writes these pairs to the ROM. Also logs the pairs to a file.
    """
    # Create the ROM table
    rom_table = RomTable()
    rom_table.create()
    # Create a sorted list of key:value pairs to be written into the ROM
    table_data = rom_table.generate_pairs(
        options=world.options,
        placed_items=placed_items,
        placed_blocks=placed_blocks,
        entrances=entrance_list,
        actor_attributes=enemy_stats,
        move_costs=move_costs,
        palettes=palette_data,
        quizzes=quiz_data,
        music_list=music_list,
        mapmirror_list=mapmirror_list,
        puzzle_list=puzzle_list,
        mystery_opts=mystery_opts
    )

    # Update table info with variable data
    end_of_content_marker = 0x4 # end of table FFFFFFFF
    end_padding = 0x10 # 4x FFFFFFFF
    len_battle_formations = sum([len(formation) for formation in battle_formations])
    len_itemhints = sum([len(itemhint_word) for itemhint_word in itemhints])

    rom_table.info["db_size"] = (  rom_table.info["header_size"]
                                 + (len(table_data) * 8)
                                 + (len_battle_formations * 4)
                                 + end_of_content_marker
                                 + (len_itemhints * 4)
                                 + end_of_content_marker
                                 + end_padding)
    rom_table.info["seed"] = seed_id
    rom_table.info["formations_offset"] = len(table_data) * 8
    rom_table.info["itemhints_offset"] = (  rom_table.info["formations_offset"]
                                          + end_of_content_marker
                                          + (len_battle_formations * 4))

    # Write data to log file
    #with open(os.path.abspath(__file__ + "/../debug/log.txt"), "w", encoding="utf-8") as log:
    #    log.write("OPTIONS:\n\n")
    #    log.write(f"Seed: 0x{seed:0X} \"{edit_seed}\"\n")
    #    for name,data in rom_table["Options"].items():
    #        log.write(f"{name:20}: {data['value']}\n")
    #    log.write("\n")

    # Modify the table data in the ROM
    changed_coin_palette = False

    # Write Output
    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    output_path = os.path.join(output_directory, f"{out_file_name}.z64")

    # copy modded file to output
    shutil.copyfile(target_modfile, output_path)

    # edit copied file with rando data
    with open(output_path, "r+b") as file:
        # Set slot auth
        file.seek(rom_table.info["auth_address"])
        file.write(world.auth)

        # Write the db header
        # file.seek(rom_table.info["address"]) # we're already here, but leaving this in case we move auth elsewhere
        file.write(rom_table.info["magic_value"].to_bytes(4, byteorder="big"))
        file.write(rom_table.info["header_size"].to_bytes(4, byteorder="big"))
        file.write(rom_table.info["db_size"].to_bytes(4, byteorder="big"))
        file.write(rom_table.info["seed"].to_bytes(4, byteorder="big"))
        file.write(rom_table.info["formations_offset"].to_bytes(4, byteorder="big"))
        file.write(rom_table.info["itemhints_offset"].to_bytes(4, byteorder="big"))

        # Write table data and generate log file
        file.seek(rom_table.info["address"] + rom_table.info["header_size"])

        for _,pair in enumerate(table_data):
            key_int = pair["key"].to_bytes(4, byteorder="big")
            value_int = pair["value"].to_bytes(4, byteorder="big")
            file.write(key_int)
            file.write(value_int)

        for formation in battle_formations:
            for formation_hex_word in formation:
                file.write(formation_hex_word.to_bytes(4, byteorder="big"))

        # Write end of formations table
        file.write(0xFFFFFFFF.to_bytes(4, byteorder="big"))

        # Write itemhint table
        for itemhint in itemhints:
            for itemhint_hex in itemhint:
                file.write(itemhint_hex.to_bytes(4, byteorder="big"))

        # Write end of item hints table
        file.write(0xFFFFFFFF.to_bytes(4, byteorder="big"))

        # Write end of db padding
        for _ in range(1, 5):
            file.write(0xFFFFFFFF.to_bytes(4, byteorder="big"))

        # Special solution for random coin palettes
        if coin_palette_data and coin_palette_targets:
            changed_coin_palette = True
            for target_rom_location in coin_palette_targets:
                file.seek(target_rom_location)
                for palette_byte in coin_palette_data:
                    file.write(palette_byte.to_bytes(4, byteorder="big"))

    if changed_coin_palette:
        recalculate_crcs(target_modfile, coin_palette_crcs)


def get_filled_node_list(world):
    placed_items = []

    for location in world.multiworld.get_locations(world.player):

        if location.address is None:
            continue

        if location.item is None:
            continue

        pm_loc: PMLocation = location
        cur_node = Node()
        cur_node.map_area = MapArea(pm_loc.map_area_id)
        cur_node.key_name_item = pm_loc.keyname
        cur_node.item_source_type = pm_loc.source_type
        cur_node.vanilla_price = pm_loc.vanilla_price
        cur_node.item_index = pm_loc.index
        cur_node.price_index = pm_loc.price_index
        cur_node.identifier = pm_loc.identifier

        if pm_loc.price_keyname != "NONE":
            cur_node.key_name_price = pm_loc.price_keyname

        if location.item.game == world.game:
            cur_node.current_item = location.item
        else:
            cur_node.current_item = item_table["Mushroom"][2]

        if "Shop" in cur_node.identifier:
            cur_node.current_item.base_price = get_shop_price(pm_loc,
                                                              world.options.include_shops.value,
                                                              world.options.merlow_rewards_pricing.value)

        placed_items.append(cur_node)

    return placed_items
