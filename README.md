# Paper Mario 64 AP World
This is the AP World for Paper Mario 64 to be used in [Archipelago](https://archipelago.gg/). It is not yet playable. 

## Setup

View the setup guide [here](https://github.com/JKBSunshine/PMR_APWorld/blob/main/docs/setup_en.md). Since the AP World is not yet playable, you cannot actually play a world created
using this AP World. What you _can_ do is generate multiworlds and view the spoiler log to see if there are any obvious
problems with the playthrough, or report any bugs you encounter while generating.

As you can see below, there is still a fair bit of legwork to be done before this AP World is playable, so make sure to
take note of what is and isn't implemented before reporting bugs. 

## TO DO

Some of these are partially implemented, some of these are mostly implemented, and some aren't even started.

- Output of a patch file that applies the desired settings, randomized items, locations, etc.
- Create yaml file using PMR settings string
- Set up a way to communicate with an AP server for sending/receiving items.
- Logic helpers to account for access rules that change depending on settings
- Logic helper to determine when to grant Parakarry check
- Logic for keysanity option: false
- Logic for gear shuffle options: vanilla and gear_locations
- Super blocks and multi-coin blocks as potential locations, as well as being able to shuffle them
- Mystery shuffle
- Formation shuffle
- Random puzzles
- Enemy difficulty
- Require Specific Spirits
- Limit Chapter Logic
- Start with random items
- Consumable item pool randomization
- Item traps
- Entrance Randomizer
- Open World settings
- Bowser Castle Mode (change entrances, remove locations)
- Power Star Hunt (logic, items, remove locations in ch8 if skipped)
- Prevent Chapter 8 locations from holding too many progression items (OoT does similar with Ganon's Castle)

## Credits

The Paper Mario Randomizer (PMR) as a whole was built by

clover
Icebound777
Pronyo

and can be found [here](https://github.com/icebound777/PMR-SeedGenerator). The AP World is being ported from PMR with their permission.

Various AP Worlds were referenced to help port PMR, including OoT, Pokemon Emerald, Subnautica, and Kingdom Hearts 2.