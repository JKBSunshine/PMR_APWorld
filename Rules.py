from typing import TYPE_CHECKING

from .data.LocationsList import exclude_from_trap_placement
from worlds.generic.Rules import set_rule, add_rule, add_item_rule
from .data.ItemList import item_multiples_ids
from .items import ap_id_to_pm_data

if TYPE_CHECKING:
    from . import PaperMarioWorld


def set_rules(world: "PaperMarioWorld") -> None:

    world.multiworld.completion_condition[world.player] = lambda state: state.has("STARROD", world.player)

    # Coin gets glitchy graphic on the sign for some reason
    add_item_rule(world.multiworld.get_location("GR Goomba Road 2 On the Sign", world.player),
                  lambda item: item.player != world.player or item.name != "Coin")

    # Items in the storeroom in the second Toad Town shop can cause a crash when entering the screen
    # This is caused by the game attempting to spawn a local item that has already been collected
    # While this shouldn't normally be possible, we're going to safeguard this from occurring+

    add_item_rule(world.multiworld.get_location("TT Residental District Storeroom Item 1", world.player),
                  lambda item: item.player != world.player or item.id not in item_multiples_ids.keys())
    add_item_rule(world.multiworld.get_location("TT Residental District Storeroom Item 2", world.player),
                  lambda item: item.player != world.player or item.id not in item_multiples_ids.keys())
    add_item_rule(world.multiworld.get_location("TT Residental District Storeroom Item 3", world.player),
                  lambda item: item.player != world.player or item.id not in item_multiples_ids.keys())
    add_item_rule(world.multiworld.get_location("TT Residental District Storeroom Item 4", world.player),
                  lambda item: item.player != world.player or item.id not in item_multiples_ids.keys())

    # Damage traps cannot be in shops or over spinning flowers
    untrappable_locations = list(filter(lambda location: location.name in exclude_from_trap_placement,
                                        world.multiworld.get_locations(player=world.player)))
    for loc in untrappable_locations:
        add_item_rule(loc, lambda item: item.player != world.player or item.name != "Damage Trap")
