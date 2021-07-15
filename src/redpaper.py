#!/usr/bin/python3
import argparse
import platform
import os
import sys
from utils import (
    colors,
    clear,
    refresh,
    message,
)
from settings import Settings
from fetch import Fetch
from setter import WallSet

system = platform.system()
start_path = os.getcwd()


class Home:
    def main_menu(self, message=message):
        refresh(message)
        choice = input(
            f"""{colors['green']}
                Welcome to Redpaper. This is a TUI used to
                control the underlying Redpaper program.
                Select an option:\n{colors['normal']}
            {colors['red']} 1 {colors['normal']}: {colors['blue']} Download wallpapers {colors['normal']} \n
            {colors['red']} 2 {colors['normal']}: {colors['blue']} Next wallpaper{colors['normal']}\n
            {colors['red']} 3 {colors['normal']}: {colors['blue']} Previous wallpaper{colors['normal']}\n
            {colors['red']} 4 {colors['normal']}: {colors['blue']} Settings{colors['normal']}\n
            {colors['red']} 5 {colors['normal']}: {colors['blue']} Help {colors['normal']}\n
            {colors['red']} x {colors['normal']}: {colors['blue']} exit {colors['normal']}\n
                >>>  """
        )
        if choice == "1":
            refresh(message)
            Fetch().wall_dl()
        elif choice == "2":
            message = f"{colors['green']} Changed wallpaper {colors['normal']}\n"
            refresh(message)
            img_path = WallSet().sequetial(0)
            WallSet().set_wallpaper(img_path)
            self.main_menu()
        elif choice == "3":
            message = f"{colors['green']} Changed wallpaper {colors['normal']}\n"
            refresh(message)
            img_path = WallSet().sequetial(1)
            WallSet().set_wallpaper(img_path)
            self.main_menu()
        elif choice == "4":
            message = ""
            Settings().main_settings()
        elif choice == "5":
            # TODO: create a help page
            message = "HELP\n"
            refresh(message)
            print(
                f"""
                {colors['green']}You can check the wiki for help:
                https://github.com/keystroke3/redpaper/wiki{colors['normal']}"""
            )
            self.main_menu()
        elif choice == "x" or choice == "X":
            clear()
        else:
            Home().main_menu()


def main():
    parser = argparse.ArgumentParser(
        description="""This is a simple program that allows you to change
    you desktop wallpaper. It fetches the best wallpapers from Reddit
    and sets one as the wallpaper."""
    )
    parser.add_argument(
        "-d", "--download", action="store_true", help="Downloads new wallpapers"
    )
    parser.add_argument(
        "-c",
        "--change",
        action="store_true",
        help="sets a wallpaper without downloading new ones",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Download new wallpapers and set one of them",
    )
    parser.add_argument(
        "-l", "--limit", help="Number of wallpapers to look for. Default = 1"
    )
    parser.add_argument(
        "-p",
        "--path",
        metavar="PATH",
        help="Sets the download location for new wallpapers\n"
        "The img_path has to be in quotes",
    )
    parser.add_argument(
        "-i", "--image", help="Sets a user specified image as wallpaper.\n"
    )
    parser.add_argument(
        "-r", "--sub", help="Sets a user specified subreddit(s) as source.\n"
    )
    parser.add_argument(
        "-f",
        "--folder",
        help="Uses images stored in the specified folders\n" "Path has to be in quotes",
    )
    parser.add_argument(
        "-s", "--settings", action="store_true", help="change settings permanently"
    )
    parser.add_argument(
        "-b", "--back", action="store_true", help="Sets the previous image as wallpaper"
    )

    # args = parser.parse_args()
    args, unknown = parser.parse_known_args()
    if not len(sys.argv) > 1:
        Home().main_menu()
    if args.settings:
        if args.path:
            Settings().change_dl_path(args.path, True)
            return
        elif args.limit:
            Settings().max_dl_choice(args.limit, True)
            return
        elif args.sub:
            Settings().change_subs(args.sub, True)
            return
        else:
            print("No option selected or selection not understood")
            return
    if args.download:
        sub_list = ""
        if args.sub:
            sub_list = args.sub
        if args.limit:
            Fetch().d_limit = int(args.limit)
        Fetch(sub_list).wall_dl()
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
    elif unknown:
        if len(unknown) == 1:
            WallSet().set_wallpaper(unknown[0])
        else:
            Fetch().custom_folder(unknown)
            args.change


if __name__ == "__main__":
    main()
