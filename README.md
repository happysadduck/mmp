# MMP
A simple Minecraft Music Player.

## Introduction
ever felt bad while coding quietly? want some music? try this one!

auto play minecraft music, with configurable time interval(I recommand 5-10min, not too noisy)

don't like some of them? you can ban as many as you want

## How to play
### Minecraft preparation
a minecraft laucher is needed, and install the newest minecraft version.

find the ".minecraft" folder. make sure the file structure is like this:

```plain
.minecraft/
├── assets/
│   ├── indexes/
│   ├── objects/
│   └── # other folders
└── # other files & folders
```
if there is no assets/indexes or no assets/objects, your minecraft might be broken, you had better to install a new laucher.

### Python preparation
Pygame is needed for the python environment that you use.

### Play!
use python to run ./mmp.py. follow the instructions, then enjoy the music!

if you want to stop the music player, the only way is to kill the process. (For example, Ctrl+C in the terminal)

when there's no remaining music, the player will automatically stops.

## Tips
If this repository is not on the same disk as .minecraft/, the music could sounds very bad. try to copy the folder into this repository(but not the whole, just the .minecraft/assets/ will be ok)