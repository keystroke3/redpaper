import os
import praw
import csv
import requests
import json
import pickle
import gi
from os.path import isfile
from PIL import Image
from io import BytesIO
from os.path import join
from utils import (
    colors,
    Spinner,
    working_dir,
    HOME,
    post_attr_file,
    wall_data_file,
    wall_names,
    parse_subs,
    pictures,
    subreddits,
    d_limit,
)

gi.require_version("Notify", "0.7")
from gi.repository import Notify  # noqa: E402

start_path = os.getcwd()


class Fetch:
    def __init__(self, sub_list=""):
        if sub_list:
            self.subreddits = parse_subs(sub_list)
        else:
            self.subreddits = subreddits

    def auth(self):
        os.chdir(working_dir)
        # Authenticate with Reddit using Auth0
        reddit = praw.Reddit(
            client_id="OTiCnaMKYCGzrA",
            client_secret=None,
            redirect_uri="http://localhost:8080",
            user_agent="UserAgent",
            commaScopes="all",
        )
        # collect data from reddit

        wallpaper = reddit.subreddit(self.subreddits)
        top_paper = wallpaper.hot(limit=d_limit)
        try:
            with open("post_attr", "w") as attrs:
                print(f"{colors['green']}Getting file attributes{colors['normal']}")
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
            exit(1)

    def wall_dl(self):
        Notify.init("Redpaper")
        Notify.Notification.new("wallpaper download started").show()
        counter = 1
        self.auth()
        with open(post_attr_file, "r") as links:
            csvread = csv.reader(links, delimiter="\t")
            for link in csvread:
                with Spinner():
                    try:
                        raw_file_name = link[0]
                        bad_chars = ("{", "}", "@", "$", "%", "^", "*", "/", "]", "[")
                        clean_chars = [c for c in raw_file_name if c not in bad_chars]
                        clean_name = "".join(clean_chars).replace(" ", "_")

                        def file_exists():
                            jpeg_file = f"{clean_name}.jpeg"
                            png_file = f"{clean_name}.png"
                            if isfile(jpeg_file):
                                return jpeg_file
                            elif isfile(png_file):
                                return png_file
                            return False

                        file_ = file_exists()
                        if file_:
                            print(
                                f"{colors['green']}{clean_name} already exists{colors['normal']}"
                            )
                            wall_names[counter] = file_
                            counter += 1
                            continue
                        else:
                            try:
                                print(
                                    f"{colors['green']}checking image properties{colors['normal']}"
                                )
                                payload = requests.get(link[1])
                                img = Image.open(BytesIO(payload.content))
                                width, height = img.size
                                ar = width / height
                                img.format.lower()
                                new_file_name = clean_name + "." + img.format.lower()
                            except Exception:
                                print(
                                    f"{colors['red']}Error Getting file ... skipping{colors['normal']}"
                                )
                                continue

                            if ar > 1.2:
                                try:
                                    r = requests.get(link[1])
                                except Exception:
                                    continue
                                try:
                                    print(
                                        f"{colors['green']}Downloading image... {colors['normal']}"
                                    )
                                    with open(new_file_name, "wb") as image:
                                        image.write(r.content)
                                        print(
                                            f"{colors['green']}{new_file_name}, saved{colors['normal']}"
                                        )
                                    wall_names[counter] = str(new_file_name)
                                    counter += 1
                                except FileNotFoundError:
                                    continue
                                except OSError:
                                    raw_name_words = clean_name.split("_")
                                    short_raw_name = "_".join(raw_name_words[:3])
                                    new_file_name = (
                                        short_raw_name + "." + img.format.lower()
                                    )
                                    with open(new_file_name, "wb") as image:
                                        image.write(r.content)
                                        print(
                                            f"{colors['green']}{new_file_name}, saved{colors['normal']}"
                                        )
                                    wall_names[counter] = str(new_file_name)

                            else:
                                print(
                                    f"{colors['yellow']} File skipped ...{colors['normal']}"
                                )
                                continue
                    except KeyboardInterrupt:
                        print("Keyboard interupt. Closing... ")
                        exit(1)
        os.chdir(working_dir)
        with open(wall_data_file, "w") as wall_data:
            json.dump(wall_names, wall_data, indent=2)
        selection_point = 0
        with open("point.pickle", "wb") as point:
            pickle.dump(selection_point, point)

        Notify.init("Redpaper")
        Notify.Notification.new("Finished downloading wallpapers").show()

    def custom_folder(self, folder_path):
        os.chdir(working_dir)
        try:
            for p in folder_path:
                if p[0] == "~":
                    p = p.replace("~", HOME)
                if p == ".":
                    p = start_path
                if not os.path.isdir(p):
                    p = join(start_path, p)
                img_list = []
                img_paths = []
                for r, d, f in os.walk(p):
                    init_img_count = len(img_list)
                    [
                        img_list.append(i)
                        for i in f
                        if ".jpg" or ".jpeg" or ".png" in i
                        for i in f
                    ]
                    final_img_count = len(img_list)
                    if final_img_count - init_img_count == 0:
                        error = f"{r} does not contain any JPEG or PNG files."
                        message = f"{colors['red_error']}{error}{colors['normal']}"
                        print(message)
                        continue
                    [img_paths.append(join(r, img)) for img in img_list]
                    message = (
                        f"{colors['green']}Added images form {r} {colors['normal']}"
                    )
                    print(message)
                img_dict = {}
                for ind, img in enumerate(img_paths, 1):
                    img_dict[ind] = img
                with open(wall_data_file, "w") as wall_data:
                    json.dump(img_dict, wall_data)
                selection_point = 0
                with open("point.pickle", "wb") as point:
                    pickle.dump(selection_point, point)
        except FileNotFoundError:
            error = "ERROR: The img_path you entered does not exist."
            message = f"{colors['red_error']}{error}{colors['normal']}"
            print(message)
