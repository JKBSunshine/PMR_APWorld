# AP World Setup
## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.4 or higher. Make sure to install the
  Generator. 
- [The Paper Mario AP World](https://github.com/JKBSunshine/PMR_APWorld/tree/main). To download it, click Code and then Download ZIP.
  - (Later this will be a release with a proper .apworld extension, but there's no point to that just yet.)
- A legally obtained Paper Mario ROM.

## Steps
1. Extract the zip file in the worlds folder of your Archipelago install. 
This is generally found at C:\ProgramData\Archipelago\lib\worlds
2. Run ArchipelagoLauncher.exe (found in the base Archipelago folder) and click Generate Template Settings to generate a 
template YAML file. It will open the folder of template files which you can then edit to your liking. 
You may also instead use the PM Sample.yaml file included in the Paper Mario AP World zip file.
3. After filling out your YAML, save it in the Players folder (found in the base Archipelago folder), 
along with any other yaml files you wish to include in the multiworld. 
4. Run ArchipelagoLauncher.exe again and click Generate, or just run ArchipelagoGenerate.exe.
5. The first time you generate, you will be asked for the location of your Paper Mario ROM file. 
6. After it is done generating, you can go to the output folder (found in the base Archipelago folder) 
to view the zip file, which contains the spoiler log and an Archipelago server file 
(and any files that other games included in the multiworld might have generated). 

At this time, you cannot play the randomized game that Archipelago generates, but you can view the spoiler log.
The spoiler log contains the locations and the items found there, the spheres in the multiworld, 
and the paths you would need to take to reach the required progression items to beat the game.

Note that since some settings are not yet implemented fully, not all of them will result in a successful generation. 
Refer to the To Do section in the main ReadMe to see if a setting is not yet implemented.
