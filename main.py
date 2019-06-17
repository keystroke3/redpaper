#! /usr/bin/env python

import argparse
import fetch
import wall_set

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

args = parser.parse_args()


def main():
    if args.download:
        print("Downloading wallpaper")
        fetch.wall_dl()
    elif args.change:
        print("changing wallpaper")
        wall_set.set_wallpaper()
    elif args.all:
        print("Download and set wallpaper")
        fetch.wall_dl()
        wall_set.set_wallpaper()
    else:
        args.parser.help()
        parser.print_help()
        # wall_set.set_wallpaper()


if __name__ == '__main__':
    main()
