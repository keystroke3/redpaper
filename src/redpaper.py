#!/usr/bin/python3
import argparse
import platform
import os
import configparser
import threading
import time
import sys
import praw
import csv
import requests
import json
import pickle
import gi
import traceback
from subprocess import call
from PIL import Image
from io import BytesIO
from os.path import join
gi.require_version('Notify', '0.7')
from gi.repository import Notify


normal = "\033[00m"
red_error = "\033[91m"
green = "\033[92m"
red = "\033[91m"
blue = "\033[94m"
yellow = "\033[93"

message = ""
global counter


wall_names = {}
counter = 1
HOME = os.environ.get("HOME")
working_dir = join(HOME, ".redpaper")
settings_file = join(working_dir, "settings.ini")
wall_data_file = join(working_dir, "wall_data.json")
post_attr_file = join(working_dir, "post_attr")
config = configparser.ConfigParser()
system = platform.system()
start_path = os.getcwd()

if not os.path.exists(settings_file):
    config['settings'] = {
        'download_dir': join(HOME, "Pictures", "Redpaper"),
        'download_limit': 5}
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)
    with open(settings_file, "w") as f:
        config.write(f)
    config.read(settings_file)
else:
    config.read(settings_file)

pictures = config['settings']['download_dir']
d_limit = int(config['settings']['download_limit'])


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def refresh():
    """Prints the bunner with whatever message from the operation
    """
    banner = """\n
    ██████╗ ███████╗██████╗ ██████╗  █████╗ ██████╗ ███████╗██████╗
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██████╔╝█████╗  ██║  ██║██████╔╝███████║██████╔╝█████╗  ██████╔╝
    ██╔══██╗██╔══╝  ██║  ██║██╔═══╝ ██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
    ██║  ██║███████╗██████╔╝██║     ██║  ██║██║     ███████╗██║  ██║"""
    red_banner = f"{red}{banner}{normal}"
    clear()
    print(red_banner)
    print(message)


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


class Fetch():
    def auth(self):
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
        subreddits = "wallpaper+wallpapers"
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

    def wall_dl(self):
        Notify.init("Redpaper")
        Notify.Notification.new("wallpaper download started").show()
        global counter
        self.auth()
        with open(post_attr_file, "r") as links:
            csvread = csv.reader(links, delimiter="\t")
            for link in csvread:
                with Spinner():
                    try:
                        raw_file_name = link[0]
                        bad_chars = ('{', '}', '@', '$', '%',
                                     '^', '*', '/', ']', '[')
                        clean_chars = [
                            c for c in raw_file_name if c not in bad_chars]
                        clean_file_name = ''.join(
                            clean_chars).replace(' ', '_')

                        if (os.path.isfile(clean_file_name + ".jpeg")):
                            print(
                                f"\t{green}{clean_file_name} already exists{normal}")
                            store_file_name = clean_file_name+".jpeg"
                            wall_names[counter] = store_file_name
                            counter += 1
                            continue
                        elif (os.path.isfile(clean_file_name + ".png")):
                            print(
                                f"\t{green}{clean_file_name} already exists{normal}")
                            file_name = clean_file_name+".png"
                            wall_names[counter] = str(file_name)
                            counter += 1
                            continue
                        else:
                            try:
                                print(
                                    f"hecking image properties{normal}")
                                image_link = link[1]
                                payload = requests.get(image_link)
                                img = Image.open(BytesIO(payload.content))
                                width, height = img.size
                                ar = width / height
                                img.format.lower()
                                new_file_name = clean_file_name+"."+img.format.lower()
                            except Exception:
                                print(
                                    f"\t{red}Error Getting file ... skipping{green}")
                                continue

                            if ar > 1.2:
                                try:
                                    r = requests.get(link[1])
                                except Exception:
                                    continue
                                try:
                                    print(
                                        f"{green}Downloading image... {green}")
                                    with open(new_file_name, "wb") as image:
                                        image.write(r.content)
                                        print(
                                            f"{green}{new_file_name}, saved{normal}")
                                    wall_names[counter] = str(new_file_name)
                                    counter += 1
                                except FileNotFoundError:
                                    continue
                                except OSError:
                                    raw_name_words = clean_file_name.split('_')
                                    short_raw_name = '_'.join(
                                        raw_name_words[:3])
                                    new_file_name = short_raw_name+"."+img.format.lower()
                                    with open(new_file_name, "wb") as image:
                                        image.write(r.content)
                                        print(
                                            f"{green}{new_file_name}, saved{normal}")
                                    wall_names[counter] = str(new_file_name)

                            else:
                                print(f"{yellow}File skipped ...{green}")
                                continue
                        print(f"{normal}")
                    except KeyboardInterrupt:
                        print("Keyboard interupt. Closing... ")
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
                    [img_list.append(i) for i in f if ".jpg" or ".jpeg" or ".png" in i for i in f]
                    final_img_count = len(img_list)
                    if final_img_count-init_img_count == 0:
                        error = f"{r} does not contain any JPEG or PNG files."
                        message = f"{red_error}{error}{normal}"
                        print(message)
                        continue
                    [img_paths.append(join(r, img)) for img in img_list]
                    message = f"{green}Added images form {r} {normal}"
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
            message = f"{red_error}{error}{normal}\n"
            print(message)


class Settings():
    def main_settings(self):
        refresh()
        choice = input(f"""{green}
                Welcome to redpaper settings menu.
                Choose an option:\n{normal}
                {red} 1 {normal}: {blue} Change download location{normal} \n
                {red} 2 {normal}: {blue} Change the download limit{normal}\n
                {red} r {normal}: {blue} Reset to default {normal}\n
                {red} h {normal}: {blue} Back to home {normal}\n
                {red} q {normal}: {blue} Quit {normal}\n
                >>>  """)
        if choice == "1":
            self.change_dl_path()
        if choice == "2":
            self.max_dl_choice()
        elif choice == "r" or choice == "R":
            self.restore_default()
            self.main_settings()
        elif choice == "h" or choice == "H":
            Home().main_menu()
        elif choice == "q" or choice == "Q":
            clear()

    def save_settings(self):
        """
        Writes the changed settings to file.
        """
        try:
            with open(settings_file, "w") as configfile:
                config.write(configfile)
                message = f"{green} Changes made successfully{normal}\n"
                print(message)
        except FileNotFoundError:
            os.mkdir(working_dir)
            with open(settings_file, "w") as f:
                f.write("")
            Settings().save_settings()

    def max_dl_choice(self, d_limit="", silent=False):
        """
        Allows the user to select a max number of wallpaper download attemts
        """

        if not silent:
            refresh()
            d_limit = input(f"""{green}
                Enter the maximum number of wallpaper to attemt to download
                The number cannot exceed 100.
                Current value is {d_limit}
                {normal}\n
                {red}x{normal}: {blue} main menu{normal}
                {red}q{normal}: {blue} Quit{normal}
                >>> """)
        try:
            max_dl = int(d_limit)
            if max_dl > 100:
                message = (
                    f"{green}Please enter a value (1 - 100){normal}\n")
                print(message)
            else:
                config.set('settings', 'download_limit', str(max_dl))
                self.save_settings()
        except TypeError:
            max_dl = str(d_limit)
            if max_dl == "x" or max_dl == "X":
                self.main_settings()
                return
            else:
                error = "You did not enter a number"
                message = f"{red_error}{error}{normal}\n"
                refresh()
                self.max_dl_choice()

    def change_dl_path(self, new_path="", silent=False):
        """
        Changes the img_path for new wallpaper downloads
        """
        if not new_path:

            refresh()
            new_path = input(f"""
                            {green}Enter the complete img_path to the new location.
                            This is case sensivite. "Pics" and "pics" are different
                            e.g. /home/user/Pictures\n
                            Current img_path is: {pictures}\n{normal}
                            {red}x{normal} : {blue}main settings{normal}
                            {red}q{normal}: {blue} Quit{normal}
                            >>> """)
        if new_path == "x":
            self.main_settings()
            return
        elif new_path == "q" or new_path == "Q":
            clear()
            return
        elif not os.path.exists(new_path):
            error = "ERROR: The img_path you entered does not exist."
            message = f"{red_error}{error}{normal}\n"
        else:
            config.set('settings', 'download_dir', str(new_path))
            Settings().save_settings()
            message = "Path changed successfully"
            print(message)
            self.change_dl_path()

    def restore_default(self):
        refresh()
        choice = input(f"""{green}
                This section allows you to reset all the settings to default.
                Note that this cannot be undone. \n{normal}
                You sure you want to continue?\n
                {green} 1: Yes {normal} \n
                {red} 2: No {normal}\n
                >>> """)
        if choice == "2":
            self.main_settings()
            return
        elif choice == "1":
            config.set('settings', 'download_dir',
                       join(HOME, "Pictures", "Redpaper"))
            config.set('settings', 'download_limit', "5")
            self.save_settings()
        else:
            error = "ERROR: Choice was not understood"
            message = f"{red_error}{error}{normal}\n"
            self.restore_default()
            return


class WallSet:
    os.chdir(working_dir)

    def check_de(self, current_de, list_of_de):
        """Check if any of the strings in ``list_of_de``
        is contained in ``current_de``."""
        return any([de in current_de for de in list_of_de])

    def sequetial(self, go_back):
        try:
            with open(wall_data_file, encoding='utf-8') as data:
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
            elif (selection_point < len(saved_walls) and
                  selection_point != 1 and go_back == 1):
                selection_point -= 1
            elif (selection_point < len(saved_walls) and
                  go_back == 0):
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
                print(f"{red}Error, file path not recognized{normal}")

        else:
            print(f"{red}Sorry, your system is not supported yet.{normal}")

    def linux_wallpaper(self, img_path):
        check_de = self.check_de
        # wall_change = self.wall_change
        de = os.environ.get('DESKTOP_SESSION')
        try:
            if check_de(de, [
                    "gnome", "gnome-xorg", "gnome-wayland", "unity", "ubuntu",
                    "ubuntu-xorg", "budgie-desktop"
            ]):
                call([
                    "gsettings", "set", "org.gnome.desktop.background",
                    "picture-uri",
                    "file://%s" % img_path
                ])

            elif check_de(de, ["cinnamon"]):
                call([
                    "gsettings", "set", "org.cinnamon.desktop.background",
                    "picture-uri",
                    "file://%s" % img_path
                ])

            # TODO: fix this code to better support pantheon

            elif check_de(de, ["mate"]):
                call([
                    "gsettings", "set", "org.mate.background", "picture-filename",
                    "'%s'" % img_path
                ])

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
                print("""\nRedpaper has run into a problem. Please raise an issue on
                https://github.com/keystroke3/redpaper/issues.
                Make sure you include this error message:\n\n""")
                print(traceback.format_exc())
                Notify.Notification.new("Redpaper encountered an issue").show()

        except Exception:
            print("""\nRedpaper has run into a problem. Please raise an issue on
                    https://github.com/keystroke3/redpaper/issues.
                    Make sure you include this error message:\n\n""")
            print(traceback.format_exc())
            Notify.Notification.new("Redpaper encountered an issue").show()


class Home():
    def main_menu(self):
        refresh()
        choice = input(f"""{green}
                Welcome to Redpaper. This is a TUI used to
                control the underlying Redpaper program.
                Select an option:\n{normal}
            {red} 1 {normal}: {blue} Download wallpapers {normal} \n
            {red} 2 {normal}: {blue} Next wallpaper{normal}\n
            {red} 3 {normal}: {blue} Previous wallpaper{normal}\n
            {red} 4 {normal}: {blue} Settings{normal}\n
            {red} 5 {normal}: {blue} Help {normal}\n
            {red} x {normal}: {blue} exit {normal}\n
                >>>  """)
        if choice == "1":
            refresh()
            Fetch().wall_dl()
        elif choice == "2":
            message = f"{green} Changed wallpaper {normal}\n"
            refresh()
            img_path = WallSet().sequetial(0)
            WallSet().set_wallpaper(img_path)
            self.main_menu()
        elif choice == "3":
            message = f"{green} Changed wallpaper {normal}\n"
            refresh()
            img_path = WallSet().sequetial(1)
            WallSet().set_wallpaper(img_path)
            self.main_menu()
        elif choice == "4":
            message = ""
            Settings().main_settings()
        elif choice == "5":
            # TODO: create a help page
            message = "HELP\n"
            refresh()
            print(f"""
                {green}You can check the wiki for help:
                https://github.com/keystroke3/redpaper/wiki{normal}""")
            self.main_menu()
        elif choice == "x" or choice == "X":
            clear()
        else:
            Home().main_menu()


def main():
    parser = argparse.ArgumentParser(
        description="""This is a simple program that allows you to change
    you desktop wallpaper. It fetches the best wallpapers from Reddit
    and sets one as the wallpaper.""")
    parser.add_argument("-d", "--download", action="store_true",
                        help="Downloads new wallpapers")
    parser.add_argument("-c", "--change", action="store_true",
                        help="sets a wallpaper without downloading new ones")
    parser.add_argument("-a", "--all", action="store_true",
                        help="Download new wallpapers and set one of them")
    parser.add_argument("-l", "--limit",
                        help="Number of wallpapers to look for. Default = 1")
    parser.add_argument("-p", "--path", metavar="PATH",
                        help="Sets the download location for new wallpapers\n"
                        "The img_path has to be in quotes")
    parser.add_argument("-i", "--image",
                        help="Sets a user specified image as wallpaper.\n"
                        "Path has to be in quotes")
    parser.add_argument("-f", "--folder", action="append", nargs='*',
                        help="Uses images stored in the specified folders\n"
                        "Path has to be in quotes")
    parser.add_argument("-s", "--settings", action="store_true",
                        help="change settings permanently")
    parser.add_argument("-b", "--back", action="store_true",
                        help="Sets the previous image as wallpaper")

    # args = parser.parse_args()
    args, unknown = parser.parse_known_args()
    if unknown:
        if len(unknown) == 1:
            WallSet().set_wallpaper(unknown[0])
        else:
            Fetch().custom_folder(unknown)
            args.change
    elif args.settings:
        if args.path:
            Settings().change_dl_path(args.path, True)
            return
        elif args.limit:
            Settings().max_dl_choice(args.limit, True)
            return
        else:
            print("No option selected or selection not understood")
            return
    if args.download:
        if args.limit:
            Fetch().d_limit = int(args.limit)
            Fetch().wall_dl()
        else:
            Fetch().wall_dl()
    elif args.change:
        if args.back:
            img_path = WallSet().sequetial(1)
            WallSet().set_wallpaper(img_path)
        else:
            img_path = WallSet().sequetial(0)
            WallSet().set_wallpaper(img_path)
    elif args.image:
        WallSet().set_wallpaper(args.image)
    elif args.folder:
        Fetch().custom_folder(args.folder[0])
        args.change
    elif args.all:
        img_path = WallSet().sequetial(0)
        if args.limit:
            Fetch().d_limit = int(args.limit)
            Fetch().wall_dl()
        WallSet().set_wallpaper(img_path)
    elif args.back:
        img_path = WallSet().sequetial(1)
        WallSet().set_wallpaper(img_path)
    else:
        Home().main_menu()

if __name__ == '__main__':
    main()
