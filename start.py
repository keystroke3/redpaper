#!/usr/bin/python3

import argparse
import os
import configparser
import fetch
import wall_set
import settings
from menu import main_menu

parser = argparse.ArgumentParser(
    description="""This is a simple program that allows you to change
    you desktop wallpaper. It fetches the best wallpapers from Reddit
    and sets a random one as the wallpaper.""")

parser.add_argument("-d", "--download", action="store_true",
                    help="Downloads new wallpapers sets one of them")
parser.add_argument("-c", "--change", action="store_true",
                    help="sets a wallpaper without getting new ones")
parser.add_argument("-a", "--all", action="store_true",
                    help="Download new wallpapers and set one of them")
parser.add_argument("-l", "--limit",
                    help="Number of wallpapers to look for. Default = 5")
parser.add_argument("-R", "--any", action="store_true",
                    help="Sets a random wallpaper form all the downloads")
parser.add_argument("-r", "--recent", action="store_true",
                    help="Sets a random wallpaper from recent downloads")
parser.add_argument("-p", "--path", metavar="path",
                    help="Sets the path where background pictures are downloaded")

args = parser.parse_args()

settings_file = settings_file = os.path.join(os.environ.get("HOME"),
                                             ".redpaper", "settings.ini")
config = configparser.ConfigParser()
config.read(settings_file)

working_dir = config['settings']['working_dir']
post_attr_file = config['settings']['post_attr_file']
wall_data_file = config['settings']['wall_data_file']
d_limit = int(config['settings']['download_limit'])


def main():
    if args.path:
        settings.change_path(args.path, True)
    if args.download:
        if args.limit:
            fetch.d_limit = int(args.limit)
            fetch.wall_dl()
        else:
            fetch.wall_dl()
    elif args.change:
        if args.any:
            wall_set.random_any()
            wall_set.set_wallpaper()
        elif args.recent:
            wall_set.random_recent()
            wall_set.set_wallpaper()
        else:
            wall_set.sequetial()
            wall_set.set_wallpaper()
    elif args.all:
        if args.limit:
            fetch.d_limit = int(args.limit)
            fetch.wall_dl()
        wall_set.sequetial()
        wall_set.set_wallpaper()
    else:
        main_menu()

if __name__ == '__main__':
    main()
