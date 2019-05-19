#!/home/ted/.pyenv/shims/python
import praw
import csv
import requests
import os
import logging
from PIL import Image
from io import BytesIO
from fractions import Fraction as fr


# define directoires
pictures = os.path.join(os.environ.get("HOME"), "Pictures", "Redpaper")
redpaper_dir = os.path.join(os.environ.get("HOME"), ".redpaper")
post_attr_file = os.path.join(os.environ.get("HOME"), ".redpaper", "post_attr")
os.chdir(redpaper_dir)


def fetch():
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

    with open(post_attr_file, "r") as links:
        csvread = csv.reader(links, delimiter="\t")
        next(links)
        for link in csvread:
            # check if the file aready exists
            file_name = link[0]+".jpg"
            if os.path.isfile(file_name) is True:
                print(f"{file_name} already exists...skipping")
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
                    except FileNotFoundError:
                        continue

                else:
                    continue

    print("Done")

fetch()
