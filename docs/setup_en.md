# AP World Setup
## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.4 or higher. Make sure to install the
  Generator. You will not be able to generate games with Paper Mario on the Archipelago site, only locally.
- [The Paper Mario AP World](https://github.com/JKBSunshine/PMR_APWorld/tree/main). To download it, go to the [latest release](https://github.com/JKBSunshine/PMR_APWorld/releases) and download the papermario.apworld file.
- A legally obtained US 1.0 Paper Mario ROM.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later

## Add the Paper Mario AP World to your Archipelago install
Place the .apworld file in the worlds folder in your Archipelago install.
This is generally found at C:\ProgramData\Archipelago\lib\worlds.

## Creating a YAML file

### Option A: Generate a template YAML using Archipelago and edit it.
Want the typical Archipelago experience? Run ArchipelagoLauncher.exe (found in the base Archipelago folder) and click 
Generate Template Settings to generate a template YAML file. It will open the folder of template files which you can 
then edit to your liking.

### Option B: Use the PM Sample.yaml file and edit it to your liking.
Want a YAML that looks like what you'd get when exporting it from the site? Grab the PM Sample.yaml file [here.](https://github.com/JKBSunshine/PMR_APWorld/blob/main/docs/PM%20Sample.yaml) 
It has all the settings and shows options for each setting as well as what is/isn't implemented. If you want to see 
the descriptions that you would see on the site, you can check out [options.py,](https://github.com/JKBSunshine/PMR_APWorld/blob/main/options.py) 
or check out option C...

### Option C: Use the PMR website to get a setting string 
Want a GUI with buttons, sliders, descriptions, and cute styling? Grab the PMR Settings String.yaml file [here.](https://github.com/JKBSunshine/PMR_APWorld/blob/main/docs/PMR%20Settings%20String.yaml)
Visit [the Paper Mario Randomizer site](https://pm64randomizer.com/) and select your settings. When you're 
ready, go to the top of the page and click the Export button. This will update the Settings String field with the 
settings you've selected. Copy that string and put it in your YAML as the value for `pmr_settings_string`. It'll look 
similar to this:  
`pmr_settings_string: (iIvejnSpf0Kdl0rbg2u0a6Om)(gb1f1p1s0Rzm2)(pSaRn1x1(pGktpbwsl))(qh3SiPZgc2ELt7DQFVO)(dd1ca1.5m1kshzw4EFlvyp0b)(xq100r0t0xubpl128)(mc150h10f5b3s0j0a0irn4x16Q)(om2btwcrFPs65796o2dz0x?50!70Y)(cm7p20g20k20o20a20b20w20s20l20x2n2e2y2c5trhdu-1j)g)`

Note that since some settings are not yet implemented fully, not all of them will result in a successful generation. 
[PM Sample.YAML](https://github.com/JKBSunshine/PMR_APWorld/blob/main/PM%20Sample.yaml) can be referred to to see what options are and are not implemented, regardless of how you choose 
to create your YAML.

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
