#!/usr/bin/python3
import threading
import time
import sys
import praw
import csv
import requests
import configparser
import os
import json
import pickle
import settings
from pathlib import Path
from PIL import Image
from io import BytesIO
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

global counter

normal = "\033[00m"
red_error = "\033[31;47m"
green = "\033[92m"
red = "\033[91m"
blue = "\033[94m"
yellow = "\033[93"

wall_names = {}
counter = 1
settings_file = settings.settings_file
config = configparser.ConfigParser()
config.read(settings_file)

working_dir = config['settings']['working_dir']
post_attr_file = config['settings']['post_attr_file']
wall_data_file = config['settings']['wall_data_file']
pictures = config['settings']['download_dir']
d_limit = int(config['settings']['download_limit'])
try:
    subreddits = config['settings']['communities']
except KeyError:
    subreddits = "wallpaper+wallpapers"


class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

def auth():
    os.chdir(working_dir)
    global counter
    # Authenticate with Reddit using Auth0
    reddit = praw.Reddit(
        client_id="OTiCnaMKYCGzrA",
        client_secret=None,
        redirect_uri="http://localhost:8080",
        user_agent="UserAgent",
        commaScopes="all",
    )
    # collect data from reddit
    wallpaper = reddit.subreddit(subreddits)

    top_paper = wallpaper.hot(limit=d_limit)
    try:
        with open("post_attr", "w") as attrs:
            print(f"{green}Getting file attributes{normal}")
            for post in top_paper:
                attrs.write(str(post.title) + "\t" + (str(post.url)))
                attrs.write("\r")
        try:
            os.chdir(pictures)
        except FileNotFoundError:
            os.mkdir(pictures)
            os.chdir(pictures)
    except KeyboardInterrupt:
        print("Keyboard interupt. Closing... ")


def wall_dl():
    from gi.repository import Notify
    Notify.init("Redpaper")
    Notify.Notification.new("wallpaper download started").show()
    global counter
    auth()
    with open(post_attr_file, "r") as links:
        csvread = csv.reader(links, delimiter="\t")
        for link in csvread:
            with Spinner():
                try:
                    raw_file_name = link[0]
                    if (os.path.isfile(raw_file_name + ".jpeg")):
                        print(f"{green}{raw_file_name} already exists{normal}")
                        store_file_name = raw_file_name+".jpeg"
                        wall_names[counter] = store_file_name
                        counter += 1
                        continue
                    elif (os.path.isfile(raw_file_name + ".png")):
                        print(f"{green}{raw_file_name} already exists{normal}")
                        file_name = raw_file_name+".png"
                        wall_names[counter] = str(file_name)
                        counter += 1
                        continue
                    else:
                        try:
                            print(f"{green}checking image properties{normal}")
                            image_link = link[1]
                            payload = requests.get(image_link)
                            img = Image.open(BytesIO(payload.content))
                            width, height = img.size
                            ar = width / height
                            img.format.lower()
                            new_file_name = raw_file_name+"."+img.format.lower()
                        except KeyboardInterrupt:
                            print("Keyboard interupt. Exiting...")
                            break
                        except:
                            print(f"{red}Error Getting file ... skipping{green}")
                            continue

                        if ar > 1.2:
                            try:
                                r = requests.get(link[1])
                            except:
                                continue
                            try:
                                print(f"{green}Downloading image... {green}")
                                with open(new_file_name, "wb") as image:
                                    image.write(r.content)
                                    print(f"{green}{new_file_name}, saved{normal}")
                                wall_names[counter] = str(new_file_name)
                                counter += 1
                            except FileNotFoundError:
                                continue

                        else:
                            print(f"{yellow}File skipped ...{green}")
                            continue
                    print(f"{normal}")
                except KeyboardInterrupt:
                    print("Keyboard interupt. Closing... ")

    os.chdir(working_dir)
    with open("wall_data.json", "w") as wall_data:
        json.dump(wall_names, wall_data, indent=2)
    selection_point = 0
    with open("point.pickle", "wb") as point:
        pickle.dump(selection_point, point)

    Notify.init("Redpaper")
    Notify.Notification.new("Finished downloading wallpapers").show()
