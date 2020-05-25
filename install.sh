#!/bin/bash

[ -d "/opt/redpaper" ] && sudo rm -r /opt/redpaper
sudo mkdir /opt/redpaper
sudo cp src/redpaper.py /opt/redpaper
sudo ln -sf /opt/redpaper/redpaper.py /usr/bin/redpaper
sudo chmod +x /opt/redpaper/redpaper.py
sudo chmod +x /usr/bin/redpaper
python3 -m pip install praw
python3 -m pip install pillow
python3 -m pip install pygobject
python3 -m pip install requests
hash -r
