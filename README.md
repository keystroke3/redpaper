# Redpaper
## Overview
Redpaper is a simple tool that is used to download and set new wallpapers.  
It gets the images from reddit.com.  

If you frequently search for, download and set wallpapers, or like to give you system  
a new look, you this tool is for you.  When you want to change the wallpaper, you simply  
run Redpaper's download tool and it will scout Reddit for the best wallpaper of the  
day and download them. You can then change the wallpaper using it.

![Main Menu](https://raw.githubusercontent.com/keystroke3/redpaper/master/screenshots/neo-redpaper.png)

## Installation
If you are running Arch or Arch-based distro, you can install from aur:
`yay -S redpaper-git`

Redpaper only works on Linux systems at the moment, therefor only people running Linux  
can use it.  
### Dependencies
* Python 3.6 or later  
* Python3-pip  
* Requests  
* Pillow  
* PyGObject  
* feh (only if you use tiling window managers)

Python3 should come by default on a Linux system, but if you are not sure if it is installed,  
you can run  `python3` in your terminal. If you get no errors, then you can proceed. If you  
get an error, you should  visit python.org to get it.  
Pip comes by default with Python. If for some reason you don't have it, you can run:  
```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```  
and then  
```python get-pip.py```
The other dependencies will be automatically installed.  
### Procedure
When the first two dependencies have been met, you can run the following command to do the install:  
```git clone https://github.com/keystroke3/redpaper.git && cd redpaper && sudo sh install.sh```

#### Tiling window managers
If you are running a tiling window manager like i3, bspwm etc.. you will need to add this to your  
autostart files e.g. ~/.config/bspwm/bspwmrc if you are using bspwm:  
```$HOME/.redpaper/wallapaper.sh```  
This line makes sure that the wallpaper you set will persist after logging in. 
## Usage
To use, simply run `redpaper` in the terminal.
Once the installation is complete, you can use Redpaper in two ways, with command mode and with  
and with interactive shell.

### Command Line Mode (CLI)
You can run the redpaper command with arguments to perform tasks The list of arguments can be
listed by  
running `redpaper -h` or `redpaper --help` The arguments are:  
``` 
  -h, --help            show this help message and exit
  -d, --download        Downloads new wallpapers
  -c, --change          sets a wallpaper without downloading new ones
  -a, --all             Download new wallpapers and set one of them
  -l NUMBER, --limit NUMBER
                        Number of wallpapers to look for. Default = 1
  -p PATH, --path PATH  Sets the download location for new wallpapers The img_path has to be
                        in quotes
  -i IMAGE_PATH, --image IMAGE_PATH
                        Sets a user specified image as wallpaper. Path has to be in quotes
  -f FOLDER_PATH, --folder FOLDER_PATH
                        Uses images stored in the specified folder Path has to be in quotes
  -s, --settings        change settings permanently
  -b, --back            Sets the previous image as wallpaper
```
### Interactive mode (TUI)
You can also run redpaper in interactive mode, that does not involve typing commands.  
To actaivate this mode, simply run redpaper without any arguments to bring it up.  
The main menu will come up as shown below:  

#### Main Menu

You can then select the action you wish to perform and the options will change depending  
on your choices. For example, selecting 1 as the option will begin downloading the wallpapers:  
This is the basic usage of the program. You can look at the settings to edit the behavior  
of the program.

#### settings
Keep in mind that these settings will be ignored when the alternative value is passed as an argument in command mode.  
The behavior of the program can be slightly modified by the user. Currently, there are only  
 a few changes that can be made. The settings are:

* Change the wallpaper download location:
  By default, downloaded wallpapers are stored in the `$HOME/Pictures/Redpaper`  
  If you wish to change, you can use the interactive mode to edit it.  
  The path must be of the form `/path/to/dir`. It must be absolute. I.e, not `~/path/to/dir`  
  If the path is not part of $HOME, then you may need to start the settings editor with root  
  privileges for the directory to be writable.  

* ~~Wallpaper selection method~~:
  This option has been removed.

* Download limit.
  The Reddit API can take many requests, but I chose to limit the maximum to 100 because  
  I thought this is a sufficient enough number. The user can set their own limit so long  
  as it is between 1 and 100.   

[Leagal stuff](https://github.com/keystroke3/redpaper/blob/master/LEAGAL.md)
