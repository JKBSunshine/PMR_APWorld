# Paper Mario 64 AP World
This is the AP World for Paper Mario 64 to be used in [Archipelago.](https://archipelago.gg/) It is in a playable, **alpha** state. Some things will work, some things will not. Things that do work might not work in a way that you would expect from a fully completed AP World. 

Please report any issues you encounter in the dev-multiplayer channel in the Paper Mario Randomizer Discord or the Paper Mario thread in the Archipelago Discord's future game design forum. Be careful using different settings that may not be fully implemented yet, as it may result in unbeatable seeds, game crashes, or generation failures.

## Setup

View the setup guide [here.](https://github.com/JKBSunshine/PMR_APWorld/blob/main/docs/setup_en.md) Along with general setup, it will include details on what settings should or should not be used. Before tweaking the base YAML, please refer to the setup guide to save yourself from trying a setting that isn't implemented.

## Quick Notes

- Consumables are unable to be received from other players (or more accurately, there is no handling for receiving consumables if your inventory is full; keeping them local avoids that problem)
- Receiving items does not have any animation; items will simply appear in your inventory.
- Off-world items do not clarify what the item is or who it belongs to in game; you will have to look at your client to see what you have sent and to who.
- Off-world items in shops and Merlow's rewards will be automatically hinted if they are progression items so that you know what is and isn't necessary to buy. Other off-world items could still be important (or unimportant), but if it isn't hinted, don't feel too bad for skipping it.
- Refer to the [PMR Wiki](https://github.com/icebound777/PMR-SeedGenerator/wiki) for help for Paper Mario Randomizer, such as commonly missed locations, general tips, and more.

## TO DO from PMR

Some of these are partially implemented, some of these are mostly implemented, and some aren't even started.

- Create yaml file using PMR settings string
- Random puzzles
- Item traps
- Dungeon Entrance Randomizer

## Credits

The Paper Mario Randomizer (PMR) as a whole was built by

clover
Icebound777
Pronyo

and can be found [here.](https://github.com/icebound777/PMR-SeedGenerator) The AP World is being ported from PMR with their permission.

Various AP Worlds were referenced to help port PMR to Archipelago, including OoT, Pokemon Emerald, Castlevania 64, Subnautica, and Kingdom Hearts 2.
