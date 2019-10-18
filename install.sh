#!/bin/bash

[ -d "/opt/redpaper" ] && rm -r /opt/redpaper
sudo mkdir /opt/redpaper
sudo cp fetch.py wall_set.py settings.py menu.py start.py /opt/redpaper
sudo ln -sf /opt/redpaper/start.py /usr/bin/redpaper
chmod +x /opt/redpaper/start.py
chmod +x /usr/bin/redpaper
python3 -m pip install praw
python3 -m pip install pillow
python3 -m pip install pygobject
python3 -m pip install requests
hash -r