# Redpaper
## Overview
Redpaper is a simple tool that is used to download and set new wallpapers.  
It gets the images from reddit.com.  

If you frequently search for, download and set wallpapers, or like to give you system  
a new look, you this tool is for you.  When you want to change the wallpaper, you simply  
run Redpaper's download tool and it will scout Reddit for the best wallpaper of the  
day and download them. You can then change the wallpaper using it.

![Main Menu](https://raw.githubusercontent.com/keystroke3/redpaper/master/screenshots/main-menu.png)

## Installation
Redpaper only works on Linux systems at the moment, therefor only people running Linux  
can use it.  
### Dependencies
* Python 3.6 or later  
* Python3-pip  
* Requests  
* Pillow  
* PyGObject

Python3 should come by default on a Linux system, but if you are not sure if it is installed,  
you can run  `python3` in your terminal. If you get no errors, then you can proceed. If you  
get an error, you should  visit python.org to get it.  
Pip comes by default with Python. If for some reason you don't have it, you can run:  
`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`  
and then  
`python get-pip.py`  
The other dependencies will be automatically installed.  
### Procedure
When the first two dependencies have been met, you can run the following command to do the install:  
`git clone https://github.com/keystroke3/redpaper.git && cd redpaper && sudo sh install.sh`  

For          information on how to use, please refer to the [Wiki](https://github.com/keystroke3/redpaper/wiki)  