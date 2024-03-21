# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/randomizer.py, pulled functions for rom-related stuff

from typing import TYPE_CHECKING, List, Tuple
import hashlib
import random
from .calculate_crc import recalculate_crcs
from .RomTable import RomTable
from worlds.Files import APContainer
import zipfile
import os

if TYPE_CHECKING:
    from . import PaperMarioWorld


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


def generate_output(world: PaperMarioWorld, output_dir: str) -> None:
    # create rom table
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
    world
):
    """
    Generates key:value pairs of locations and items from a randomized item set
    and writes these pairs to the ROM. Also logs the pairs to a file.
    """
    # Create the ROM table
    rom_table = RomTable()
    rom_table.create()
