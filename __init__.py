import logging
import threading
import copy
import functools
import settings
import typing
import os
from typing import List, AbstractSet, Union, Dict, Any  # remove when 3.8 support is dropped
from collections import Counter, deque
from string import printable
from BaseClasses import (Region, Entrance, Location, Item, Tutorial,
                         CollectionState, MultiWorld, LocationProgressType, ItemClassification as ic)
from Options import Range, Toggle, VerifyKeys, Accessibility
from worlds.AutoWorld import World, WebWorld
from . import Locations, options
from .data.enum_types import BlockType
from .data.maparea import MapArea
from .modules.random_audio import get_randomized_audio
from .modules.random_map_mirroring import get_mirrored_map_list
from .modules.random_movecosts import get_randomized_moves
from .modules.random_palettes import get_randomized_palettes
from .Regions import PMRegion
from .RuleParser import Rule_AST_Transformer
from .Entrance import PMEntrance
from .Utils import data_path, read_json
from .Locations import PMLocation, location_factory, location_name_to_id
from .ItemPool import generate_itempool
from .items import PMItem, pm_is_item_of_type, pm_data_to_ap_id
from .data.ItemList import item_table, item_groups, progression_miscitems
from .data.itemlocation_special import limited_by_item_areas
from .data.itemlocation_replenish import replenishing_itemlocations
from .data.LocationsList import location_table, location_groups
from .modules.random_actor_stats import get_shuffled_chapter_difficulty
from .data import regions
from .Rules import set_rules
from .modules.random_partners import get_rnd_starting_partners
from .options import EnemyDifficulty, PaperMarioOptions, ShuffleKootFavors, PartnerUpgradeShuffle, HiddenBlockMode, GearShuffleMode
from .data.node import Node
from .Rom import generate_output
from Fill import fill_restrictive
from .modules.random_blocks import get_block_placement
import pkg_resources

logger = logging.getLogger("Paper Mario")


class PMSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Paper Mario 1.0 ROM"""
        description = "Paper Mario ROM File"
        copy_to = "Paper Mario.z64"

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
                    true  for operating system default program
        Alternatively, a path to a program to open the .z64 file with
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True


# information for the supported games setup guide; set up to make it easier to add more guides
class PaperMarioWeb(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A Guide to setting up the Paper Mario randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["JKB"]
    )

    # set tutorials to the list of each setup
    tutorials = [setup]


# all_locations = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}


class PaperMarioWorld(World):
    """
    Paper Mario is a turn-based adventure RPG. Bowser has kidnapped Princess Peach along with her castle using the
    power of the Star Rod, which grants the wishes of the holder. You must rescue the Star Spirits so that they can
    help you take back the Star Rod from Bowser and save Peach. You will have to defeat powerful foes
    and venture through dangerous lands with the help of partners you meet along the way.
    """
    game = "Paper Mario"
    web = PaperMarioWeb()
    topology_present = True
    options_dataclass = PaperMarioOptions
    options = PaperMarioOptions
    settings: typing.ClassVar[PMSettings]
    item_name_to_id = {item_name: pm_data_to_ap_id(data, False) for item_name, data in item_table.items()}
    location_name_to_id = location_name_to_id

    item_name_groups = item_groups
    location_name_groups = location_groups

    data_version = 1
    required_client_version = (0, 4, 4)
    auth: bytes

    def __init__(self, multiworld, player):
        super(PaperMarioWorld, self).__init__(multiworld, player)

        # For generation
        self.placed_items = []
        self.placed_blocks = {}

        self._regions_cache = {}
        self.parser = Rule_AST_Transformer(self, self.player)

        self.regions = []
        self.starting_items = Counter()

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        if not os.path.exists(cls.settings.rom_file):
            raise FileNotFoundError(cls.settings.rom_file)

    # Do some housekeeping before generating, namely fixing some options that might be incompatible with each other
    def generate_early(self) -> None:

        # Make sure it doesn't try to shuffle Koot coins if rewards aren't shuffled
        if self.options.koot_favors.value == ShuffleKootFavors.option_Vanilla:
            self.options.koot_coins.value = False

        # turn off individual partner toggles if starting with random partners was selected
        if self.options.start_random_partners.value:
            self.options.start_with_goombario.value = False
            self.options.start_with_kooper.value = False
            self.options.start_with_bombette.value = False
            self.options.start_with_parakarry.value = False
            self.options.start_with_bow.value = False
            self.options.start_with_watt.value = False
            self.options.start_with_sushie.value = False
            self.options.start_with_lakilester.value = False

        # turn on random partner if no partners were selected; debatable whether to use min/max here or set both to 1.
        elif not (self.options.start_with_goombario.value or self.options.start_with_kooper.value
                  or self.start_with_bombette.value or self.options.start_with_parakarry.value
                  or self.options.start_with_bow.value or self.start_with_watt.value
                  or self.options.start_with_sushie.value or self.options.start_with_lakilester.value):
            self.options.start_random_partners.value = True

        # swap mins and maxes so the min isn't bigger than the max
        self.options.min_start_partners.value, self.options.max_start_partners.value = (
            min([self.options.min_start_partners.value, self.options.max_start_partners.value]),
            max(self.options.min_start_partners.value, self.options.max_start_partners.value))

        self.options.min_start_items.value, self.options.max_start_items.value = (
            min([self.options.min_start_items.value, self.options.max_start_items.value]),
            max(self.options.min_start_items.value, self.options.max_start_items.value))

        if self.options.start_random_partners.value:
            starting_partners = get_rnd_starting_partners(self.options.min_start_partners.value,
                                                          self.options.max_start_partners.value)

            for partner in starting_partners:
                if partner == "Goombario":
                    self.options.start_with_goombario.value = True
                elif partner == "Kooper":
                    self.options.start_with_kooper.value = True
                elif partner == "Bombette":
                    self.options.start_with_bombette.value = True
                elif partner == "Parakarry":
                    self.options.start_with_parakarry.value = True
                elif partner == "Bow":
                    self.options.start_with_bow.value = True
                elif partner == "Watt":
                    self.options.start_with_watt.value = True
                elif partner == "Sushie":
                    self.options.start_with_sushie.value = True
                elif partner == "Lakilester":
                    self.options.start_with_lakilester.value = True

        # limit chapter logic only applies when using the specific star spirits setting
        if not self.options.require_specific_spirits.value:
            self.options.limit_chapter_logic.value = False

        # shuffle blocks if necessary
        # place blocks if not done already
        if not self.placed_blocks:
            self.placed_blocks = get_block_placement(self.options.super_multi_blocks.value,
                                                     self.options.partner_upgrades.value >=
                                                     PartnerUpgradeShuffle.option_Super_Block_Locations)

    def create_regions(self) -> None:
        # Create base regions
        menu = PMRegion("Menu", self.player, self.multiworld)
        start = PMEntrance(self.player, self.multiworld, 'New Game', menu)
        menu.exits.append(start)
        self.multiworld.regions.append(menu)

        # Load region json files
        for file in pkg_resources.resource_listdir(__name__, "data/regions"):
            if not pkg_resources.resource_isdir(__name__, "data/regions/" + file):
                self.load_regions_from_json(data_path("regions", file))
        start.connect(self.get_region("Gate District Mario's House Pipe"))

        self.parser.create_delayed_rules()

        # Connect exits
        for region in self.regions:
            for exit in region.exits:
                exit.connect(self.get_region(exit.vanilla_connected_region))

    def create_items(self) -> None:
        generate_itempool(self)

        # Starting inventory
        # Gear
        for boots in range(1, self.options.starting_boots.value + 2):
            self.multiworld.push_precollected(self.create_item(f"BootsProxy{boots}"))

        for hammer in range(1, self.options.starting_hammer.value + 2):
            self.multiworld.push_precollected(self.create_item(f"HammerProxy{hammer}"))

        # Partners
        if self.options.start_with_goombario.value:
            self.multiworld.push_precollected(self.create_item("Goombario"))
        if self.options.start_with_kooper.value:
            self.multiworld.push_precollected(self.create_item("Kooper"))
        if self.options.start_with_bombette.value:
            self.multiworld.push_precollected(self.create_item("Bombette"))
        if self.options.start_with_parakarry.value:
            self.multiworld.push_precollected(self.create_item("Parakarry"))
        if self.options.start_with_bow.value:
            self.multiworld.push_precollected(self.create_item("Bow"))
        if self.options.start_with_watt.value:
            self.multiworld.push_precollected(self.create_item("Watt"))
        if self.options.start_with_sushie.value:
            self.multiworld.push_precollected(self.create_item("Sushie"))
        if self.options.start_with_lakilester.value:
            self.multiworld.push_precollected(self.create_item("Lakilester"))

        self.itempool, self.pre_fill_items = self.divide_itempools()

        self.multiworld.itempool += self.itempool

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self):

        self.auth = self.random.getrandbits(16 * 8).to_bytes(16, "little")

        # remove internal event locations that are not going to exist in this seed
        all_state = self.get_state_with_complete_itempool()
        all_locations = self.get_locations()
        all_state.sweep_for_events(locations=all_locations)
        reachable = self.multiworld.get_reachable_locations(all_state, self.player)
        unreachable = [loc for loc in all_locations if
                       loc.internal and loc.event and loc.locked and loc not in reachable]
        for loc in unreachable:
            loc.parent_region.locations.remove(loc)

        if self.options.open_forest.value:
            loc = self.multiworld.get_location("Southern District Fice T. Forest Pass", self.player)
            loc.parent_region.locations.remove(loc)

    def modify_multidata(self, multidata: dict):
        import base64
        # Replace connect name
        multidata['connect_names'][base64.b64encode(self.auth).decode("ascii")] = multidata['connect_names'][
            self.multiworld.player_name[self.player]]

    def load_regions_from_json(self, file_path):
        region_json = read_json(file_path)

        for region in region_json:
            new_region = PMRegion(region['region_name'], self.player, self.multiworld)
            if 'map_id' in region:
                new_region.map_id = region['map_id']
            if 'area_id' in region:
                new_region.font_color = region['area_id']
            if 'map_name' in region:
                new_region.scene = region['map_name']
            if 'locations' in region:
                for location, rule in region['locations'].items():
                    new_location = location_factory(location, self.player)
                    new_location.parent_region = new_region
                    new_location.rule_string = rule
                    self.parser.parse_spot_rule(new_location)
                    if new_location.never:
                        # We still need to fill the location even if ALR is off.
                        logger.debug('Unreachable location: %s', new_location.name)
                    new_location.player = self.player
                    new_region.locations.append(new_location)
            if 'events' in region:
                for event, rule in region['events'].items():
                    # Allow duplicate placement of events
                    lname = '%s from %s' % (event, new_region.name)
                    new_location = PMLocation(self.player, lname, event=True, parent=new_region)
                    new_location.rule_string = rule
                    self.parser.parse_spot_rule(new_location)
                    if new_location.never:
                        logger.debug('Dropping unreachable event: %s', new_location.name)
                    else:
                        new_location.player = self.player
                        new_region.locations.append(new_location)
                        self.make_event_item(event, new_location)
                        new_location.show_in_spoiler = False
            if 'exits' in region:
                for exit, rule in region['exits'].items():
                    new_exit = PMEntrance(self.player, self.multiworld, '%s -> %s' % (new_region.name, exit), new_region)
                    new_exit.vanilla_connected_region = exit
                    new_exit.rule_string = rule
                    self.parser.parse_spot_rule(new_exit)
                    if new_exit.never:
                        logger.debug('Dropping unreachable exit: %s', new_exit.name)
                    else:
                        new_region.exits.append(new_exit)

            self.multiworld.regions.append(new_region)
            self.regions.append(new_region)
            self._regions_cache[new_region.name] = new_region

    # Note on allow_arbitrary_name:
    # PM defines many helper items and event names that are treated indistinguishably from regular items,
    #   but are only defined in the logic files. This means we need to create items for any name.
    # Allowing any item name to be created is dangerous in case of plando, so this is a middle ground.
    def create_item(self, name: str, allow_arbitrary_name: bool = False):
        if name in item_table:
            return PMItem(name, self.player, item_table[name], False)
        if allow_arbitrary_name:
            return PMItem(name, self.player, ('Event', ic.progression, None, None, False, False, False), True)
        raise Exception(f"Invalid item name: {name}")

    def make_event_item(self, name, location, item=None):
        if item is None:
            item = self.create_item(name, allow_arbitrary_name=True)
        self.multiworld.push_item(location, item, collect=False)
        location.locked = True
        location.event = True
        if name not in item_table:
            location.internal = True
        return item

    def divide_itempools(self):
        main_items = []
        prefill_item_names = []
        dungeon_restricted_items = {}

        # progression items that need to be in replenishable locations
        for item in progression_miscitems:
            prefill_item_names.append(item)

        # key items shuffled within their own dungeons
        if not self.options.keysanity.value:
            for dungeon in limited_by_item_areas:
                for itemlist in limited_by_item_areas[dungeon].values():
                    for item in itemlist:
                        assert item not in dungeon_restricted_items
                        dungeon_restricted_items[item] = dungeon
                        prefill_item_names.append(item.name)

        # gear items shuffled among gear locations
        if self.options.gear_shuffle_mode.value == GearShuffleMode.option_Gear_Location_Shuffle:
            for item in self.itempool:
                if item.name in item_groups["Gear"]:
                    prefill_item_names.append(item.name)

        # upgrades shuffled among super blocks
        if self.options.partner_upgrades.value == PartnerUpgradeShuffle.option_Super_Block_Locations:
            for item in self.itempool:
                if item.name in item_groups["PartnerUpgrade"]:
                    prefill_item_names.append(item.name)

        prefill_items = []
        for item in self.itempool:
            if item.name in prefill_item_names and item not in prefill_items:
                prefill_items.append(item)
            else:
                main_items.append(item)

        return main_items, prefill_items

    # handle player-specific stuff like cosmetics, audio, enemy stats, etc.

    # only returns proper result after create_items and divide_itempools are run
    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self):

        def prefill_state(base_state):
            state = base_state.copy()
            for item in self.get_pre_fill_items():
                self.collect(state, item)
            state.sweep_for_events(locations=self.get_locations())
            return state

        # Prefill required replenishable items, local key items depending on settings
        items = self.get_pre_fill_items()
        locations = list(self.multiworld.get_unfilled_locations(self.player))
        self.multiworld.random.shuffle(locations)

        # Set up initial state
        state = CollectionState(self.multiworld)
        for item in self.itempool:
            self.collect(state, item)
        state.sweep_for_events(locations=self.get_locations())

        # place progression items that are also consumables in locations that are replenishable
        replenish_locations = [name for name, data in location_table.items() if data[0] in replenishing_itemlocations]
        replenish_items = list(filter(lambda item: item.name in progression_miscitems, self.pre_fill_items))

        for item in replenish_items:
            self.pre_fill_items.remove(item)

        locations = list(filter(lambda location: location.name in replenish_locations,
                                             self.multiworld.get_unfilled_locations(player=self.player)))

        self.multiworld.random.shuffle(locations)
        fill_restrictive(self.multiworld, prefill_state(state), locations, replenish_items,
                         single_player_placement=True, lock=True, allow_excluded=True)

        # Place gear items in gear locations
        if self.options.gear_shuffle_mode.value == GearShuffleMode.option_Gear_Location_Shuffle:
            gear_items = list(filter(lambda item: pm_is_item_of_type(item, "GEAR"), self.pre_fill_items))
            gear_locations = location_groups["Gear"]
            locations = list(filter(lambda location: location.name in gear_locations,
                                    self.multiworld.get_unfilled_locations(player=self.player)))
            if isinstance(locations, list):
                for item in gear_items:
                    self.pre_fill_items.remove(item)
                self.multiworld.random.shuffle(locations)
                fill_restrictive(self.multiworld, prefill_state(state), locations, gear_items,
                                 single_player_placement=True, lock=True, allow_excluded=True)

        # Place partner upgrade items in super block turned yellow block locations
        if self.options.partner_upgrades.value == PartnerUpgradeShuffle.option_Super_Block_Locations:
            upgrade_items = list(filter(lambda item: pm_is_item_of_type(item, "PARTNERUPGRADE"), self.pre_fill_items))
            yellow_block_locations = [name for (name, value) in self.placed_blocks.items() if value == BlockType.YELLOW]
            locations = list(filter(lambda location: location.name in yellow_block_locations,
                                    self.multiworld.get_unfilled_locations(player=self.player)))
            if isinstance(locations, list):
                for item in upgrade_items:
                    self.pre_fill_items.remove(item)
                self.multiworld.random.shuffle(locations)
                fill_restrictive(self.multiworld, prefill_state(state), locations, upgrade_items,
                                 single_player_placement=True, lock=True, allow_excluded=True)

        # Place dungeon key items in their own dungeon
        if not self.options.keysanity:
            dungeon_restricted_items = {}
            for dungeon in limited_by_item_areas:
                key_items = []
                locations = [name for name, data in location_table.items() if data[0][:3] == dungeon]
                for itemlist in limited_by_item_areas[dungeon].values():
                    for item in itemlist:
                        assert item not in dungeon_restricted_items
                        dungeon_restricted_items[item] = dungeon
                        key_items.append(item)
                        self.pre_fill_items.remove(item)
                if isinstance(locations, list):
                    self.multiworld.random.shuffle(locations)
                    fill_restrictive(self.multiworld, prefill_state(state), locations, key_items,
                                     single_player_placement=True, lock=True, allow_excluded=True)

    def generate_output(self, output_directory: str):
        generate_output(self, output_directory)

    def get_locations(self):
        return self.multiworld.get_locations(self.player)

    def get_location(self, location):
        return self.multiworld.get_location(location, self.player)

    def get_region(self, region_name):
        try:
            return self._regions_cache[region_name]
        except KeyError:
            ret = self.multiworld.get_region(region_name, self.player)
            self._regions_cache[region_name] = ret
            return ret

    # Specifically ensures that only real items are gotten, not any events.
    def get_state_with_complete_itempool(self):
        all_state = CollectionState(self.multiworld)
        for item in self.itempool + self.pre_fill_items:
            self.multiworld.worlds[item.player].collect(all_state, item)
        all_state.stale[self.player] = True

        return all_state

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "power_star_hunt"
        )
        return slot_data


