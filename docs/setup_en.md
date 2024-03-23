# AP World Setup
## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.4 or higher. Make sure to install the
  Generator. 
- [The Paper Mario AP World](https://github.com/JKBSunshine/PMR_APWorld/tree/main). To download it, click Code and then Download ZIP.
  - (Later this will be a release with a proper .apworld extension, but there's no point to that just yet.)
- A legally obtained Paper Mario ROM, with the latest base rando patch applied to it. The patch file can typically be found in the [PMR GitHub](https://github.com/icebound777/PMR-SeedGenerator/tree/main/res)

## Steps
1. Extract the zip file in the worlds folder of your Archipelago install. 
This is generally found at C:\ProgramData\Archipelago\lib\worlds
2. Run ArchipelagoLauncher.exe (found in the base Archipelago folder) and click Generate Template Settings to generate a 
template YAML file. It will open the folder of template files which you can then edit to your liking. 
You may also instead use the PM Sample.yaml file included in the Paper Mario AP World zip file.
3. After filling out your YAML, save it in the Players folder (found in the base Archipelago folder), 
along with any other yaml files you wish to include in the multiworld. 
4. Run ArchipelagoLauncher.exe again and click Generate, or just run ArchipelagoGenerate.exe.
5. The first time you generate, you will be asked for the location of your modded Paper Mario ROM file. 
6. After it is done generating, you can go to the output folder (found in the base Archipelago folder) 
to view the zip file, which contains the spoiler log, the patched rom, and an Archipelago server file 
(and any files that other games included in the multiworld might have generated). 

Note that since some settings are not yet implemented fully, not all of them will result in a successful generation. 
Refer to the To Do section in the main ReadMe to see if a setting is not yet implemented.

At this time, it can successfully patch a modded rom into a playable solo seed. I have not yet done excessive testing to check for crashes, unbeatable seeds, or anything else. It's very possible that certain workarounds implemented to help get to this point will make it impossible to beat the game for technical or logical reasons; please report these if you find any. For instance, a likely issue (I think) will be that keys that there are multiples of will not work properly.
