import os
import threading
import time
import configparser
import sys
from xdg.BaseDirectory import xdg_cache_home
from os.path import join


colors = {
    "normal": "\033[00m",
    "red_error": "\033[91m",
    "green": "\033[92m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "yellow": "\033[93m",
}

message = ""
wall_names = {}
HOME = os.environ.get("HOME")

working_dir = join(xdg_cache_home, "redpaper")
settings_file = join(working_dir, "settings.ini")
wall_data_file = join(working_dir, "wall_data.json")
post_attr_file = join(working_dir, "post_attr")


conf = configparser.ConfigParser()


def get_config():
    if not os.path.exists(settings_file):
        conf["settings"] = {
            "download_dir": join(HOME, "Pictures", "Redpaper"),
            "subreddits": "wallpaper+wallpapers",
            "download_limit": 5,
        }
        if not os.path.exists(working_dir):
            os.mkdir(working_dir)
        with open(settings_file, "w") as f:
            conf.write(f)
    conf.read(settings_file)
    return conf


config = get_config()
pictures = config["settings"]["download_dir"]
d_limit = int(config["settings"]["download_limit"])
try:
    subreddits = config["settings"]["subreddits"]
except KeyError:
    subreddits = "wallpaper+wallpapers"


def parse_subs(subs_list):
    if type(subs_list) == str:
        if " " in subs_list:
            subreddits = subs_list.replace(" ", "+")
        elif "," in subs_list:
            subreddits = subs_list.replace(",", "+")
        else:
            subreddits = subs_list
        return subreddits


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def refresh(message):
    """Prints the bunner with whatever message from the operation"""
    banner = """\n
    ██████╗ ███████╗██████╗ ██████╗  █████╗ ██████╗ ███████╗██████╗
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██████╔╝█████╗  ██║  ██║██████╔╝███████║██████╔╝█████╗  ██████╔╝
    ██╔══██╗██╔══╝  ██║  ██║██╔═══╝ ██╔══██║██╔═══╝ ██╔══╝  ██╔══██
    ██║  ██║███████╗██████╔╝██║     ██║  ██║██║     ███████╗██║  ██║"""
    red_banner = f"{colors['red']}{banner}{colors['normal']}"
    clear()
    print(red_banner)
    print(message)


class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in "|/-\\":
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
            sys.stdout.write("\b")
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False
