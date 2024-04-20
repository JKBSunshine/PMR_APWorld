from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule, add_rule
from .options import HiddenBlockMode
from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from . import PaperMarioWorld


def set_rules(world: "PaperMarioWorld") -> None:

    world.multiworld.completion_condition[world.player] = lambda state: state.has("STARROD", world.player)

    def can_flip_panels(state: "CollectionState") -> bool:
        return state.has("Ultra_Hammer", world.player) or state.has("Super_Boots", world.player)

    # This also applies to breaking yellow blocks, though the game never tells you that you can use Bombette
    def can_shake_trees(state: "CollectionState") -> bool:
        return state.has("Bombette", world.player) or state.has("Hammer", world.player)

    def can_hit_grounded_blocks(state: "CollectionState") -> bool:
        return state.has("Bombette", world.player) or \
               state.has("Kooper", world.player) or \
               state.has("Hammer", world.player) or \
               state.has("Super_Boots", world.player)

    # Floating blocks here refers to those at normal height, not the high ones that require ultra boots.
    def can_hit_floating_blocks(state: "CollectionState") -> bool:
        return state.has("Kooper", world.player) or \
               state.has("Boots", world.player)

    def can_hit_grounded_switches(state: "CollectionState") -> bool:
        return state.has("Bombette", world.player) or \
               state.has("Kooper", world.player) or \
               state.has("Hammer", world.player) or \
               state.has("Boots", world.player) or \
               state.has("Parakarry", world.player)
    
    # Steps are not literal stairs, but terrain too tall to walk up, requiring you to jump (or use Parakarry)
    # Jumping gains more height than Parakarry, so not all 'steps' can be climbed with Parakarry
    # Parakarry also cannot be used to go forward or back, only left or right
    # If logic requires boots, Parakarry is likely either unable to be used there or requires overly-precise positioning
    def can_climb_steps(state: "CollectionState") -> bool:
        return state.has("Parakarry", world.player) or state.has("Boots", world.player)
    
    # Hidden blocks normally require Watt's ability to see; Players can choose to make them always visible.
    def can_see_hidden_blocks(state: "CollectionState") -> bool:
        return (state.has("Watt", world.player) or 
                world.options.hidden_block_mode.value == HiddenBlockMode.option_Always_Visible)
    
    # To unlock Parakarry, you need 3 letters. In vanilla these are all on Mt Rugged, but here any 3 letters will do
    def has_parakarry_letters(state: "CollectionState") -> bool:
        return state.has_group("Letters", world.player, 3)

    def saved_all_yoshi_kids(state: "CollectionState") -> bool:
        return state.has("'RF_SavedYoshiKid1'", world.player) and \
               state.has("'RF_SavedYoshiKid2'", world.player) and \
               state.has("'RF_SavedYoshiKid3'", world.player) and \
               state.has("'RF_SavedYoshiKid4'", world.player) and \
               state.has("'RF_SavedYoshiKid5'", world.player)

    # Landing on a pipe is required to reenter it, and you cannot
    def can_reenter_vertical_pipes(state: "CollectionState") -> bool:
        return state.has("Kooper", world.player) or \
               state.has("Boots", world.player) or \
               state.has("Parakarry", world.player)
    
    def can_reach_star_way(state: "CollectionState") -> bool:
        if world.options.star_hunt_skips_ch8.value:
            return False
        elif world.options.power_star_hunt.value:
            return state.has_group("PowerStar", world.player, world.options.required_power_stars.value)
        else:
            return star_spirit_count(state) >= world.options.star_spirits_required.value

    def star_spirit_count(state: "CollectionState") -> int:
        spirits = 0
        for spirit_number in range (1, 8):
            if state.has(f"STARSPIRIT_{spirit_number}", world.player):
                spirits += 1

        return spirits
