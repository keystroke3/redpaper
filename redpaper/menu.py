#!/usr/bin/python3
import configparser
import fetch
import wall_set
from settings import main_settings
from settings import clear
from settings import banner
config = configparser.ConfigParser()


def Red():
    global message
    red_banner = f"{red}{banner}{normal}"
    clear()
    print(red_banner)
    print(message)


global message
message = ""

normal = "\033[00m"
red_error = "\033[31;47m"
green = "\033[92m"
red = "\033[91m"
blue = "\033[94m"


def exit_choice(*args):
    if args[0].__name__ == "set_wallpaper":
        stay = input(f"""\n
                {red} 1 {normal}: {blue} Main menu {normal}\n
                {red} 2 {normal}: {blue} Previous Wallpaper {normal}\n
                {red} 3 {normal}: {blue} Next Wallpaper {normal}\n
                {red} x {normal}: {blue} exit {normal}\n
                >>>  """)
    else:
        stay = input(f"""\n
        {red} 1 {normal}: {blue} Main menu {normal}\n
        {Red} x {normal}: {blue} exit {normal}\n
        >>>  """)
    if stay == "1":
        main_menu()
    elif stay == "2":
        wall_set.go_back = 1
        wall_set.set_wallpaper()
        Red()
        exit_choice(args[0])
    elif stay == "3":
        wall_set.set_wallpaper()
        Red()
        exit_choice(args[0])
    elif stay == "x" or stay == "X":
        clear()


def main_menu():
    global message
    Red()
    choice = input(f"""{green}
            Welcome to Redpaper. This is a TUI used to
            control the underlying Redpaper program.
            Select an option:\n{normal}
           {red} 1 {normal}: {blue} Download wallpapers {normal} \n
           {red} 2 {normal}: {blue} Change wallpaper{normal}\n
           {red} 3 {normal}: {blue} Settings{normal}\n
           {red} 4 {normal}: {blue} Help {normal}\n
           {red} x {normal}: {blue} exit {normal}\n
            >>>  """)
    if choice == "1":
        message = ""
        Red()
        fetch.wall_dl()
        exit_choice(fetch.wall_dl)
    if choice == "2":
        message = f"{green} Changed wallpaper {normal}\n"
        Red()
        wall_set.set_wallpaper()
        exit_choice(wall_set.set_wallpaper)
    elif choice == "3":
        message = ""
        main_settings()
    elif choice == "4" or choice == "R":
        # TODO: create a help page
        message = "HELP\n"
        Red()
        print(f"""
              {green}You can check the wiki for help:
              https://github.com/keystroke3/redpaper/wiki{normal}""")
        exit_choice()
    elif choice == "x" or choice == "X":
        clear()
    else:
        main_menu()
