# AP World Setup
## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.4 or higher. Make sure to install the
  Generator. You will not be able to generate games with Paper Mario on the Archipelago site, only locally.
- [The Paper Mario AP World](https://github.com/JKBSunshine/PMR_APWorld/tree/main). To download it, click Code and then Download ZIP.
- A legally obtained, vanilla Paper Mario ROM.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later

## Add the Paper Mario AP World to your Archipelago install
Place the .apworld file in the worlds folder in your Archipelago install.
This is generally found at C:\ProgramData\Archipelago\lib\worlds.

## Creating a YAML file
- Option A: Run ArchipelagoLauncher.exe (found in the base Archipelago folder) and click Generate Template Settings to generate a 
template YAML file. It will open the folder of template files which you can then edit to your liking.
- Option B (recommended): Use the PM Sample.yaml file [here.](https://github.com/JKBSunshine/PMR_APWorld/blob/main/PM%20Sample.yaml) You may edit it to your liking. It will also tell you what settings there are and what is/isn't implemented.

Note that since some settings are not yet implemented fully, not all of them will result in a successful generation. [PM Sample.YAML](https://github.com/JKBSunshine/PMR_APWorld/blob/main/PM%20Sample.yaml) can be referred to to see what options are and are not implemented.

## Generating a Game
Follow [the general Archipelago instructions](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game) for generating a game, specifically on your local installation. You cannot generate games using the Paper Mario AP World on the website.

## Hosting a Game
Follow [the general Archipelago instructions](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) for hosting an Archipelago server. You _can_ host games that use the Paper Mario AP World on the website, or you can host it locally.

## Connecting to an Archipelago Server
1. Obtain your .appm64 file from whoever is hosting the game. These files will not upload to the website even if it is hosted there, so you will have to send/receive them elsewhere.
2. Once you have obtained your .appm64 patch file, open up ArchipelagoLauncher.exe from the base Archipelago folder and click "Open Patch". In the prompt that comes up, choose your .appm64 file. If this is your first time opening the patch file, you will be prompted to locate your vanilla ROM. You will also be prompted to locate your BizHawk client, which is named EmuHawk.exe in your BizHawk install. A patched .z64 file will be created in the same place as the patch file.
3. Once the patch file has been created, BizHawk should start up automatically with the patched ROM. The Generic BizHawk Client for Archipelago will also open, as well as a Lua Console window. At this point all you need to do to connect is enter your room's address and port (e.g. archipelago.gg:38281) into the top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is perfectly safe to make progress offline; everything will re-sync when you reconnect.

Note: After the first time you open an .appm64 file through the Archipelago Launcher, it should associate that file type with the launcher and all you should have to do is double click them.
