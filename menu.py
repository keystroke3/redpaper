#!/usr/bin/python3
import configparser
import os
import fetch
import wall_set
from settings import set_settings
from settings import main_settings

config = configparser.ConfigParser()
banner = """
██████╗ ███████╗██████╗ ██████╗  █████╗ ██████╗ ███████╗██████╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╔╝█████╗  ██║  ██║██████╔╝███████║██████╔╝█████╗  ██████╔╝
██╔══██╗██╔══╝  ██║  ██║██╔═══╝ ██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██║  ██║███████╗██████╔╝██║     ██║  ██║██║     ███████╗██║  ██║
\n
<<<<<<<<<<<<<<<<<<<<<<<<<< MAIN MENU >>>>>>>>>>>>>>>>>>>>>>>>>>>
"""


def Red():
    global message
    red_banner = f"{red}{banner}{normal}"
    os.system('cls' if os.name == 'nt' else 'clear')
    print(red_banner)
    print(message)

global message
message = ""

normal = "\033[00m"
red_error = "\033[31;47m"
green = "\033[92m"
red = "\033[91m"
blue = "\033[94m"


def quit_choice():
    stay = input(f"""\n
            {red} 1 {normal}: {blue} Main menu {normal}\n
            {red} q {normal}: {blue} Quit {normal}\n
            >>>  """)
    if stay == "1":
        main_menu()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        return


def main_menu():
    global message
    message = ""
    Red()
    choice = input(f"""
            {green}
            Welcome to Redpaper. This is a sudo-GUI used to
            control the underlying Redpaper program.\n{normal}
            
            Select an option:\n
           {red} 1 {normal}: {blue} Download wallpapers {normal} \n
           {red} 2 {normal}: {blue} Change wallpaper{normal}\n
           {red} 3 {normal}: {blue} Settings{normal}\n
           {red} 4 {normal}: {blue} Help {normal}\n
           {red} q {normal}: {blue} Quit {normal}\n
            >>>  """)
    if choice == "1":
        message = f"{green} Downloading wallpapers...{normal}\n"
        Red()
        fetch.wall_dl()
        quit_choice()
    if choice == "2":
        message = f"{green} Changing wallpaper...{normal}\n"
        Red()
        wall_set.set_wallpaper()
        quit_choice()
    elif choice == "3":
        main_settings()
    elif choice == "4" or choice == "R":
        message = "HELP\n"
        Red()
        print(f"""{green}for help please refer to the Wiki:https://github.com/keystroke3/redpaper/wiki{normal}""")
        quit_choice()
    elif choice == "q" or choice == "Q":
        os.system('cls' if os.name == 'nt' else 'clear')
main_menu()
