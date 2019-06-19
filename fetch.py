#!/usr/bin/python3
import praw
import csv
import requests
import os
import json
import pickle
from PIL import Image
from io import BytesIO

global counter
# define directoires
pictures = os.path.join(os.environ.get("HOME"), "Pictures", "Redpaper")
working_dir = os.path.join(os.environ.get("HOME"), ".redpaper")
post_attr_file = os.path.join(os.environ.get("HOME"), ".redpaper", "post_attr")
# saved_walls = os.path.join(os.environ.get("HOME"), ".redpaper", "saved")
d_limit = 5
wall_names = {}
counter = 1


def dir_check():
    if not os.path.exists(pictures):
        os.mkdir(pictures)
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)


def auth():
    os.chdir(working_dir)
    global counter
    # Authenticate with Reddit using Auth0
    reddit = praw.Reddit(client_id="OTiCnaMKYCGzrA",
                         client_secret=None,
                         redirect_uri="http://localhost:8080",
                         user_agent="UserAgent",
                         commaScopes="all",
                         )
    # collect data from reddit
    wallpaper = reddit.subreddit("wallpaper+wallpapers")

    top_paper = wallpaper.hot(limit=d_limit)

    with open("post_attr", "w") as attrs:
        print("Writing attributes")
        for post in top_paper:
            attrs.write(str(post.title)+"\t"+(str(post.url)))
            attrs.write("\r")
    os.chdir(pictures)


def wall_dl():
    dir_check()
    global counter
    auth()
    with open(post_attr_file, "r") as links:
        csvread = csv.reader(links, delimiter="\t")

        for link in csvread:
            # check if the file aready exists
            file_name = link[0]+".jpg"
            if os.path.isfile(file_name) is True:
                print(f"{file_name} already exists...skipping")
                wall_names[counter] = str(file_name)
                counter += 1
                # with open(saved_walls, "a") as s:
                #             s.write(file_name)
                #             s.write("\n")

                continue
            else:
                try:
                    print("checking image size")
                    image_link = link[1]
                    payload = requests.get(image_link)
                    img = Image.open(BytesIO(payload.content))
                    width, height = img.size
                    ar = width/height
                except:
                    print("Error Getting file ... skipping")
                    continue

                if ar > 1.2:
                    try:
                        r = requests.get(link[1])
                    except:
                        continue

                    try:
                        print("Downloading image... ")
                        with open(file_name, "wb") as image:
                            image.write(r.content)
                            print(file_name, "saved")
                        wall_names[counter] = str(file_name)
                        counter += 1

                    except FileNotFoundError:
                        continue

                else:
                    print("File skipped ...")
                    continue

    os.chdir(working_dir)
    with open("wall_data.json", "w") as wall_data:
        json.dump(wall_names, wall_data, indent=2)
    selection_point = 0
    with open("point.pickle", "wb") as point:
        pickle.dump(selection_point, point)
