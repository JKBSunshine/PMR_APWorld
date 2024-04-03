# Paper Mario 64 AP World
This is the AP World for Paper Mario 64 to be used in [Archipelago.](https://archipelago.gg/) It is in a playable, **alpha** state. Some things will work, some things will not. Things that do work might not work in a way that you would expect from a fully completed AP World. 

Please report any issues you encounter in the dev-multipler channel in the Paper Mario Randomizer Discord or the Paper Mario thread in the Archipelago Discord's future game design forum. Be careful using different settings that may not be fully implemented yet, as it may result in unbeatable seeds, game crashes, or generation failures.

## Setup

View the setup guide [here.](https://github.com/JKBSunshine/PMR_APWorld/blob/main/docs/setup_en.md) Along with general setup, it will include details on what settings should or should not be used. Before tweaking the base YAML, please refer to the setup guide to save yourself from trying a setting that isn't implemented.

## Quick Notes

- Consumables, coins, and some other items are unable to be received from other players
- Receiving items does not have any animation; items will simply appear in your inventory.
- Off-world items that are in replenishable locations (shops, trees, bushes, etc) can be collected over and over again, but will only actually send once. Do not buy them from shops repeatedly, unless you are aiming to tip the shopkeeper.
- Refer to the [PMR Wiki](https://github.com/icebound777/PMR-SeedGenerator/wiki) for help for Paper Mario Randomizer, such as commonly missed locations, general tips, and more.
  
## TO DO from PMR

Some of these are partially implemented, some of these are mostly implemented, and some aren't even started.

- Create yaml file using PMR settings string
- Logic for gear shuffle options: vanilla and gear_locations
- Mystery shuffle
- Formation shuffle
- Random puzzles
- Enemy difficulty
- Require Specific Spirits
- Limit Chapter Logic
- Start with random items
- Item traps
- Dungeon Entrance Randomizer
- Bowser Castle Mode (change entrances, remove locations)
- Power Star Hunt (logic, items, remove locations in ch8 if skipped)
- Prevent Chapter 8 locations from holding too many progression items (OoT does similar with Ganon's Castle)

## Credits

The Paper Mario Randomizer (PMR) as a whole was built by

clover
Icebound777
Pronyo

and can be found [here.](https://github.com/icebound777/PMR-SeedGenerator) The AP World is being ported from PMR with their permission.

Various AP Worlds were referenced to help port PMR to Archipelago, including OoT, Pokemon Emerald, Castlevania 64, Subnautica, and Kingdom Hearts 2.
