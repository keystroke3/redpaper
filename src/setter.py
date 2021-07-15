import platform
import os
import json
import pickle
import gi
import traceback
from subprocess import call
from os.path import join
from utils import (
    colors,
    working_dir,
    HOME,
    wall_data_file,
    pictures,
)
from fetch import Fetch

gi.require_version("Notify", "0.7")
from gi.repository import Notify  # noqa: E402

system = platform.system()
start_path = os.getcwd()


class WallSet:
    os.chdir(working_dir)

    def check_de(self, current_de, list_of_de):
        """Check if any of the strings in ``list_of_de``
        is contained in ``current_de``."""
        return any([de in current_de for de in list_of_de])

    def sequetial(self, go_back):
        try:
            with open(wall_data_file, encoding="utf-8") as data:
                saved_walls = json.load(data)
        except (FileNotFoundError, ValueError):
            Fetch().wall_dl()
        """chooses the wallpaper in the order in which they were downloaded"""
        with open(wall_data_file, "r") as data:
            saved_walls = json.load(data)

        with open("point.pickle", "rb+") as wall_point:
            # selection_point stores the value of the current wallpaper
            # it is necessary so that wallpapers don't repeat
            selection_point = pickle.load(wall_point)

            if selection_point > len(saved_walls):
                selection_point = 1
            elif selection_point == len(saved_walls) and go_back == 1:
                selection_point -= 1
            elif selection_point == len(saved_walls) and go_back == 0:
                selection_point = 1
            elif (
                selection_point < len(saved_walls)
                and selection_point != 1
                and go_back == 1
            ):
                selection_point -= 1
            elif selection_point < len(saved_walls) and go_back == 0:
                selection_point += 1
            elif (
                selection_point < len(saved_walls)
                and selection_point == 1
                and go_back == 0
            ):
                selection_point += 1
            elif (
                selection_point < len(saved_walls)
                and selection_point == 1
                and go_back == 1
            ):
                selection_point = len(saved_walls)
            elif (
                selection_point < len(saved_walls)
                and selection_point == 0
                and go_back == 0
            ):
                selection_point = 1
            elif (
                selection_point < len(saved_walls)
                and selection_point == 0
                and go_back == 1
            ):
                selection_point = len(saved_walls)
            img_name = str(saved_walls.get(str(selection_point)))
        # the new value of selection point is stored for the next run
        print(f"selection point is {selection_point}")
        with open("point.pickle", "wb") as point:
            pickle.dump(selection_point, point)
        return join(pictures, str(img_name))

    def set_wallpaper(self, img_path):
        if system == "Linux":
            if "~" in img_path:
                img_path = img_path.replace("~", HOME)
            if img_path == ".":
                img_path = start_path
            if os.path.isfile(img_path):
                self.linux_wallpaper(img_path)
            elif os.path.isfile(join(start_path, img_path)):
                self.linux_wallpaper(join(start_path, img_path))
            elif os.path.isdir(img_path):
                Fetch().custom_folder([img_path])
            elif os.path.isdir(join(start_path, img_path)):
                Fetch().custom_folder([join(start_path, img_path)])
            else:
                print(
                    f"{colors['red']}Error, file path not recognized{colors['normal']}"
                )

        else:
            print(
                f"{colors['red']}Sorry, your system is not supported yet.{colors['normal']}"
            )

    def linux_wallpaper(self, img_path):
        check_de = self.check_de
        # wall_change = self.wall_change
        de = os.environ.get("DESKTOP_SESSION")
        try:
            if check_de(
                de,
                [
                    "gnome",
                    "gnome-xorg",
                    "gnome-wayland",
                    "unity",
                    "ubuntu",
                    "ubuntu-xorg",
                    "budgie-desktop",
                ],
            ):
                call(
                    [
                        "gsettings",
                        "set",
                        "org.gnome.desktop.background",
                        "picture-uri",
                        "file://%s" % img_path,
                    ]
                )

            elif check_de(de, ["cinnamon"]):
                call(
                    [
                        "gsettings",
                        "set",
                        "org.cinnamon.desktop.background",
                        "picture-uri",
                        "file://%s" % img_path,
                    ]
                )

            # TODO: fix this code to better support pantheon

            elif check_de(de, ["mate"]):
                call(
                    [
                        "gsettings",
                        "set",
                        "org.mate.background",
                        "picture-filename",
                        "'%s'" % img_path,
                    ]
                )

            elif check_de(de, ["xfce", "xubuntu"]):
                raise TypeError
                # props = check_de(['xfconf-query', '-c', 'xfce4-desktop', '-p',
                #                   '/backdrop', '-l'])\
                #     .decode("utf-8").split('\n')
                # for prop in props:
                #     if "last-image" in prop or "image-path" in prop:
                #         call([
                #             "xfconf-query", "-c", "xfce4-desktop", "-p", prop,
                #             "-s", "''"
                #         ])
                #         call([
                #             "xfconf-query", "-c", "xfce4-desktop", "-p", prop,
                #             "-s"
                #             "'%s'" % img_path
                #         ])
                #     if "image-show" in prop:
                #         call([
                #             "xfconf-query", "-c", "xfce4-desktop", "-p", prop,
                #             "-s", "'true'"
                #         ])

            elif check_de(de, ["lubuntu", "Lubuntu"]):
                call(["pcmanfm", "-w", "%s" % img_path])

            elif check_de(de, ["sway"]):
                call(["swaymsg", "output * bg %s fill" % img_path])
            else:
                raise TypeError

        except TypeError:
            try:
                call(["xwallpaper", "--zoom", img_path])
                with open("wallpaper.sh", "w") as start:
                    start.write(f'xwallpaper --zoom "{img_path}"')
                call(["chmod", "+x", "wallpaper.sh"])
            except Exception:
                print(
                    """\nRedpaper has run into a problem. Please raise an issue on
                https://github.com/keystroke3/redpaper/issues.
                Make sure you include this error message:\n\n"""
                )
                print(traceback.format_exc())
                Notify.Notification.new("Redpaper encountered an issue").show()

        except Exception:
            print(
                """\nRedpaper has run into a problem. Please raise an issue on
                    https://github.com/keystroke3/redpaper/issues.
                    Make sure you include this error message:\n\n"""
            )
            print(traceback.format_exc())
            Notify.Notification.new("Redpaper encountered an issue").show()
