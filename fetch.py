#!/home/ted/.pyenv/shims/python
import praw
import csv
import requests
import os
import logging
from PIL import Image
from io import BytesIO
from fractions import Fraction as fr

from wall_set import set_wallpaper


# define directoires
pictures = os.path.join(os.environ.get("HOME"), "Pictures", "Redpaper")
redpaper_dir = os.path.join(os.environ.get("HOME"), ".redpaper")
post_attr_file = os.path.join(os.environ.get("HOME"), ".redpaper", "post_attr")
saved_walls = os.path.join(os.environ.get("HOME"), ".redpaper", "saved")

os.chdir(redpaper_dir)


def auth():
    # Authenticate with Reddit using Auth0
    reddit = praw.Reddit(client_id="OTiCnaMKYCGzrA",
                         client_secret=None,
                         # password = "digitalcreations1",
                         redirect_uri="http://localhost:8080",
                         user_agent="UserAgent",
                         commaScopes="all",
                         # username = "byteoverload"
                         )

    # collect data from reddit
    wallpaper = reddit.subreddit("wallpaper+wallpapers")
    top_paper = wallpaper.hot(limit=10)

    with open("post_attr", "w") as attrs:
        print("Writing attributes")
        for post in top_paper:
            attrs.write(str(post.title)+"\t"+(str(post.url)))
            attrs.write("\r")
    os.chdir(pictures)


def wall_dl():
    auth()
    with open(post_attr_file, "r") as links:
        csvread = csv.reader(links, delimiter="\t")
        next(links)
        if os.path.isfile(saved_walls) is True:
            os.remove(saved_walls)

        for link in csvread:
            # check if the file aready exists
            file_name = link[0]+".jpg"
            if os.path.isfile(file_name) is True:
                print(f"{file_name} already exists...skipping")
                with open(saved_walls, "a") as s:
                            s.write(file_name)
                            s.write("\n")
                continue
            else:
                try:
                    print("checking image size")
                    image_link = link[1]
                    payload = requests.get(image_link)
                    img = Image.open(BytesIO(payload.content))
                    width, height = img.size
                    ar = str(fr(width, height))
                except:
                    print("Error Getting file")
                    continue

                if ar == "16/9" or ar == "16/10":
                    try:
                        r = requests.get(link[1])
                    except:
                        continue

                    try:
                        print("Downloading image... ")
                        with open(file_name, "wb") as image:
                            image.write(r.content)
                            print(file_name, "saved")
                        with open(saved_walls, "a") as s:
                            s.write(file_name)
                            s.write("\n")

                    except FileNotFoundError:
                        continue

                else:
                    print("File skipped ...")
                    continue

    print("Done downloading")
