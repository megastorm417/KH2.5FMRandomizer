# Description
This is a KH2FM randomizer made to be compatible with the PS3 Version and PS2 Versions of KH2.
The PS3 Version has more ram and is also recommended but also has its downsides when compared to the PS2 Version
The PS3 Version also takes a bit longer to extract & decrypt.

# Known bugs
	-PS3 Version - Sephiroth crashes the game with his first attack
	-PS3 Version - Viewing the Item shop crashes the game
	-PS3 Version - Some bosses can cause random crashes not present in the PS2 Version
	-PS3 Version - Crashes seem to be very easily triggered?
	-PS2 Version - Game frequently runs low on memory leaving very little RAM space for enemies to spawn in (EX: Land of dragons mission 2)
	-PS2 Version - Low memory leading to crashes on room spawns, T-Posing enemies and characters, Mickey softlocking the game on spawn
	-All Versions -Some bosses may use a room changing attack which can leave the player falling endlessly
	-All Versions -Xigbar's Boss battle room has a open area allowing you to leave (Xigbar usually has a invisible wall that blocks it normally but when replaced it is removed)
	-All Versions -Equipping a keyblade before becoming KH2 Sora crashes/creates errors
	-All Versions -Gummiship skip code only works once
	-All Versions -Demyx doesn't stagger when the game can't find Demyx water clone data in a specific world (TT and HB have it)

# TODO's:
	-Randomize world progression (EX: Instead of beasts castle and land of dragons, Halloween Town and Port Royal)
	-Give HUD elements in the prologue (Find code somehow)
	-Extra randomization?

# Running
To randomize for the PS2 Version, you must have KH2Toolkit in the same folder as the randomizer.exe 
From there, you can select the ISO, ROM directory and English patch if you have one.
On your first randomization the program will extract KH2 data into a folder called "export"
If you wish to refresh your files you can hit the button in the Options tab.
It will be placed in the ROM directory when done with a custom name.

For the PS3 Version, it will extract in the same folder name "export" so make sure to clear/rename it if you randomized for a PS2 version.
You also must have index.dat from the KH2.5 Folder inside the program directory
located in "\BLES####\PS3_GAME\USRDIR\KH2Image" # being the region (US/PAL only for now)
along with HasherHD.exe, HashPairsHD.log, make_npdata.exe, and sdata-tool.exe.
It will possibly take a long time to extract based on disk speeds but you only have to do this once.



# Building a exe:
Run PYInstaller with main.py with also a custom main.spec to include icon data info as:
datas = [('icon.ico', '.')]
then run with --onefile to create one singular file.

# Credits:
	-KH2FM modding community for their documentation of data
	-Govanify's toolkit
	-TruthKey's original ARD randomizer code
	-CrazyCat00's original HasherHD program and KH2 Hex to Text Tables
