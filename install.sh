#!/bin/bash

sudo mkdir /opt/redpaper
sudo cp fetch.py wall_set.py main.py /opt/redpaper
cp point.pickle post_attr wall_data.json
sudo ln -sf /opt/redpaper/main.py /usr/bin/redpaper
chmod +x /opt/redpaper/main.py
chmod +x /usr/bin/redpaper
hash -r