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
### Usage
For          information on how to use, please refer to the [Wiki](https://github.com/keystroke3/redpaper/wiki)  

## Disclaimers and legal notices
This program was created with the mind to help community.  
It comes as is without any warranty. The creaters of this app do not claim responsibility for  
any system issues the user may encounter as a result of using this software  
This software uses publicly avaliable resources and does not claim ownership of the images  
it downloads.  
The creaters of this software have no control over the content of the images.  
If the user encounters an  image that is deemed inappropriate offencieve or illigal,  
a concern should be raised with the image hosts and not the software creaters.  
## Contributions 
Contributions are very welcome! If you like the project and wish to the project just fork the project,  
make the changes and create a pull request.  
The only rules are: Document the code you write and adhere to pep8.  
TODO List:  
_Short Term (1-2 wks)_  
- [] Add ability to change settings in the command mode
- [] Create an NSFW option
- [] Create option to choose subreddit dow download from
- [] Create an about section  

_Medium Term (4-6 wks)_
- [] Fix mandatory first run download
- [] Add project to PIP
- [] Add project to AUR
- [] Create a snap and flatpak
- [] Create a GUI
- [] Daemonize the program (make it run in the background)
- [] Add keyboard shortcuts 
 
_Long term (8-1 wks)_   
- [] Create support for Mac OS  
- [] Create support for Windows  
- [] Add other service like Unsplash and flickr  
- [] Add wallpaper category selection  
