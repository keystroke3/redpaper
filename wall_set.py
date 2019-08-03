#!/usr/bin/python3

import os
import sys
import platform
import random
import json
import pickle
import configparser
from subprocess import Popen
from fetch import pictures, working_dir, wall_dl, wall_data_file
import settings

normal = "\033[00m"
red_error = "\033[31;47m"
green = "\033[92m"
red = "\033[91m"
blue = "\033[94m"

settings_file = settings.settings_file
config = configparser.ConfigParser()
config.read(settings_file)
wall_selection_method = config['settings']['wallpaper_selection_method']
go_back = 0

path = ""
# pictures = fetch.pictures
system = platform.system()

os.chdir(working_dir)


def load_data():
    try:
        with open(wall_data_file, encoding='utf-8') as data:
            saved_walls = json.load(data)
    except (FileNotFoundError, ValueError):
            wall_dl()


def random_any():
    """Selects a random file from all the previous downloads"""
    global path
    load_data()
    selected = random.choice(os.listdir(pictures))
    path = os.path.join(pictures, selected)


def random_recent():
    """ Chooses a random file from the recently downloaded files"""
    global path
    load_data()
    random_key = str(random.randint(1, len(saved_walls)))
    random_selected = str(saved_walls.get(random_key))
    path = os.path.join(pictures, random_selected)


def sequetial():
    global path
    load_data()
    """chooses the wallpaper in the order in which they were downloaded"""
    with open(wall_data_file, "r") as data:
        saved_walls = json.load(data)
    with open("point.pickle", "rb+") as wall_point:
        # selection_point is used to store the value of the current wallpaper
        # it is necessary to have so that wallpapers don't repeat themselves
        selection_point = pickle.load(wall_point)
        print("selection point = ", selection_point)
        # the value of selection_point will be loaded and incrimened evrytime
        # this finction is run.
        if selection_point > len(saved_walls):
            selection_point = 1
        elif selection_point == len(saved_walls) and go_back == 1:
            selection_point -= 1
        elif selection_point == len(saved_walls) and go_back == 0:
            selection_point = 1
        elif (selection_point < len(saved_walls) and
              selection_point != 1 and go_back == 1):
            selection_point -= 1
        elif (selection_point < len(saved_walls) and go_back == 0):
            selection_point += 1
        elif (selection_point < len(saved_walls) and
              selection_point == 1 and go_back == 0):
            selection_point += 1
        elif (selection_point < len(saved_walls) and
              selection_point == 1 and go_back == 1):
            selection_point = len(saved_walls)
        elif (selection_point < len(saved_walls) and
              selection_point == 0 and go_back == 0):
            selection_point = 1
        elif (selection_point < len(saved_walls) and
              selection_point == 0 and go_back == 1):
            selection_point = len(saved_walls)
        img_name = str(saved_walls.get(str(selection_point)))
        path = os.path.join(pictures, str(img_name))
    # the new value of selection point is stored for the next run
    with open("point.pickle", "wb") as point:
        pickle.dump(selection_point, point)


def wall_change(*popenargs, timeout=None, **kwargs):
    """Run command with arguments.  Wait for command to complete or
    timeout, then return the returncode attribute.
    The arguments are the same as for the Popen constructor.  Example:
    retcode = call(["ls", "-l"])
    """
    with Popen(*popenargs, **kwargs) as p:
        try:
            return p.wait(timeout=timeout)
        except:  # Including KeyboardInterrupt, wait handled that.
            p.kill()
            # We don't call p.wait() again as p.__exit__ does that for us.
            raise


def set_wallpaper():
    if system == "Linux":
        if wall_selection_method == "sequential":
            sequetial()
        elif wall_selection_method == "random_any":
            random_any()
        elif wall_selection_method == "random_recent":
            random_recent()
        linux_wallpaper()
    else:
        print(f"{red}Sorry, you system is not supported at the moment{normal}")


def check_de(current_de, list_of_de):
    """Check if any of the strings in ``list_of_de``
     is contained in ``current_de``."""
    return any([de in current_de for de in list_of_de])


def linux_wallpaper():
    de = os.environ.get('DESKTOP_SESSION')
    try:
        if check_de(de, [
                "gnome", "gnome-xorg", "gnome-wayland", "unity", "ubuntu",
                "ubuntu-xorg", "budgie-desktop"
        ]):
            wall_change([
                "gsettings", "set", "org.gnome.desktop.background",
                "picture-uri",
                "file://%s" % path
            ])

        elif check_de(de, ["cinnamon"]):
            wall_change([
                "gsettings", "set", "org.cinnamon.desktop.background",
                "picture-uri",
                "file://%s" % path
            ])

        # TODO: fix this code to better support pantheon

        elif check_de(de, ["mate"]):
            wall_change([
                "gsettings", "set", "org.mate.background", "picture-filename",
                "'%s'" % path
            ])

        elif check_de(de, ["xfce", "xubuntu"]):
            # Light workaround here, just need to toggle the wallpaper
            #  from null to the original filename
            # xfconf props aren't 100% consistent so light workaround
            #  for that too
            props = check_output(['xfconf-query', '-c', 'xfce4-desktop', '-p',
                                  '/backdrop', '-l'])\
                .decode("utf-8").split('\n')
            for prop in props:
                if "last-image" in prop or "image-path" in prop:
                    wall_change([
                        "xfconf-query", "-c", "xfce4-desktop", "-p", prop,
                        "-s", "''"
                    ])
                    wall_change([
                        "xfconf-query", "-c", "xfce4-desktop", "-p", prop,
                        "-s"
                        "'%s'" % path
                    ])
                if "image-show" in prop:
                    wall_change([
                        "xfconf-query", "-c", "xfce4-desktop", "-p", prop,
                        "-s", "'true'"
                    ])

        elif check_de(de, ["lubuntu", "Lubuntu"]):
            wall_change(["pcmanfm", "-w", "%s" % path])

        elif check_de(de, ["i3", "bspwm"]):
            wall_change(["feh", "--bg-fill", path])
            with open("wallpaper.sh", "w") as start:
                start.write(f'feh --bg-fill "{path}"')
            from subprocess import call
            call(["chmod", "+x", "wallpaper.sh"])

        elif check_de(de, ["sway"]):
            wall_change(["swaymsg", "output * bg %s fill" % path])

        else:
            print("Your DE could not be detected to set the wallpaper. "
                  "You need to set the 'setcommand' paramter at"
                  "~/.config/wallpaper-reddit. "
                  "When you get it working, please file an issue.")
            # sys.exit(1)

    except:
        import traceback
        print(traceback.format_exc())
        print(f"{green}You can raise the issue with the devs here: {normal}"
              f"{green}https://github.com/keystroke3/redpaper/issues{normal}")
