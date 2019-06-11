#!/usr/bin/env python3


import argparse
import fetch
import wall_set

parser = argparse.ArgumentParser(
    description="Choose change or Download wallpaper")

parser.add_argument("-d", "--download", action="store_true",
                    help="Downloads new wallpapers sets them the wallpaper")
parser.add_argument("-c", "--change", action="store_true",
                    help="sets them the wallpaper without getting new ones")
args = parser.parse_args()


def main():
    if args.download:
        print("Downloading wallpaper")
        fetch.wall_dl()
    elif args.change:
        print("changing wallpaper")
        wall_set.set_wallpaper()
    else:
        print("No args were passed")
        fetch.wall_dl()
        # wall_set.set_wallpaper()


if __name__ == '__main__':
    main()
