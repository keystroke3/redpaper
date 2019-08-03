#!/usr/bin/python3
import configparser
import os
# from menu import main_menu
config = configparser.ConfigParser()

# Color pallete
normal = "\033[00m"
red_error = "\033[31;47m"
green = "\033[92m"
red = "\033[91m"
blue = "\033[94m"


settings_file = os.path.join(os.environ.get("HOME"), ".redpaper",
                             "settings.ini")
working_dir = os.path.join(os.environ.get("HOME"), ".redpaper")


config['settings'] = {
    'download_dir':
    os.path.join(os.environ.get("HOME"), "Pictures", "Redpaper"),
    'working_dir': os.path.join(os.environ.get("HOME"), ".redpaper"),
    'post_attr_file': os.path.join(os.environ.get("HOME"), ".redpaper",
                                   "post_attr"),
    'wall_data_file': os.path.join(os.environ.get("HOME"), ".redpaper",
                                   "wall_data.json"),
    'Wallpaper_selection_method': "sequential",
    'download_limit': 1,
    'subreddit': "wallpaper+wallpapers",
}


def set_settings():
    """
    Writes the changed settings to file.
    """
    global message
    try:
        with open(settings_file, "w") as configfile:
            config.write(configfile)
            message = f"{green} Changes made successfully{normal}\n"
    except FileNotFoundError:
            os.mkdir(working_dir)
            with open(settings_file, "w") as f:
                f.write("")
            set_settings()


if not os.path.exists(settings_file):
    set_settings()
else:
    config.read(settings_file)

working_dir = config['settings']['working_dir']
pictures = config['settings']['download_dir']
d_limit = int(config['settings']['download_limit'])
wall_selection_method = config['settings']['wallpaper_selection_method']
subreddit = config['settings']['subreddit']

global message
message = ""
banner = """██████╗ ███████╗██████╗ ██████╗  █████╗ ██████╗ ███████╗██████╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╔╝█████╗  ██║  ██║██████╔╝███████║██████╔╝█████╗  ██████╔╝
██╔══██╗██╔══╝  ██║  ██║██╔═══╝ ██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██║  ██║███████╗██████╔╝██║     ██║  ██║██║     ███████╗██║  ██║"""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def Red():
    """Prints the bunner with whatever message from the operation
    """
    global message
    red_banner = f"{red}{banner}{normal}"
    clear()
    print(red_banner)
    print(message)


def max_dl_choice(d_limit="", silent=False):
    """
    Allows the user to select a maximum number of wallpaper download attemts
    """
    global message
    if not silent:
        Red()
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
            message = (f"{green}Please enter a value less than 100{normal}\n")
            if silent:
                print(message)
        else:
            config.set('settings', 'download_limit', str(max_dl))
            set_settings()
            if silent:
                print("Changes made successfully!")
            return
            if not silent:
                main_settings()
    except ValueError:
            max_dl = str(d_limit)
            if max_dl == "x" or max_dl == "X":
                main_settings()
                return
            elif silent:
                print("Value error encountered")
            else:
                error = "You did not enter a number"
                message = f"{red_error}{error}{normal}\n"
                Red()
                max_dl_choice()


def change_path(new_path="", silent=False):
    """
    Changes the path for new wallpaper downloads
    """
    if not new_path:
        global message
        Red()
        new_path = input(f"""
                        {green}Enter the complete path to the new location.
                        This is case sensivite. "Pics" and "pics" are different
                        e.g. /home/user/Pictures\n
                        Current path is: {pictures}\n{normal}
                        {red}x{normal} : {blue}main settings{normal}
                        {red}q{normal}: {blue} Quit{normal}
                        >>> """)
    if new_path == "x":
        main_settings()
        return
    elif new_path == "q" or new_path == "Q":
        clear()
        return
    elif not os.path.exists(new_path):
        error = "ERROR: The path you entered does not exist."
        message = f"{red_error}{error}{normal}\n"
    else:
        config.set('settings', 'download_dir', str(new_path))
        set_settings()
        if silent:
            print("Path changed successfully")
    if not silent:
        change_path()


def change_subreddit():
    """
    Allows the user to change the subreddit where we fetch the pictures from
    """
    global message
    Red()
    new_subreddit = input(f"""
                           {green}Enter the just the name of the subreddit.
                           Example wallpapers for reddit.com/r/wallpapers\n
                           Current path is: {subreddit}\n{normal}
                           {red}x{normal} : {blue}main settings{normal}
                           {red} q {normal}: {blue} Quit {normal}
                           >>> """)
    if new_subreddit == "x":
        main_settings()
        return
    else:
        config.set('settings', 'subreddit', str(new_subreddit))
        set_settings()
        Red()
        change_subreddit()
        return


def wall_selection():
    """
    Allows the user to specify the method to be used when choosing wallpapers
    """
    global message
    Red()
    selection_mode = input(f"""{green}
            select one option bellow to change how wallpapers are selected\n
            {normal}
            {red} 1 {normal}: {blue} completely random{normal}\n
            {red} 2 {normal}: {blue} from lastest downloads random order
            {normal}
            {red} 3 {normal}: {blue} from latest downloads in download order
            {normal}
            {red} x {normal}: {blue} main settings {normal}\n
            {red} q {normal}: {blue} Quit {normal}\n
            >>>
            """)
    if selection_mode == "1":
        config.set('settings', 'Wallpaper_selection_method',
                   "random_any")
        set_settings()
    elif selection_mode == "2":
        config.set('settings', 'Wallpaper_selection_method',
                   "random_recent")
        set_settings()
    elif selection_mode == "3":
        config.set('settings', 'Wallpaper_selection_method',
                   "sequential")
        set_settings()
    elif selection_mode == "x" or selection_mode == "X":
        main_settings()
        return
    elif selection_mode == "q" or selection_mode == "Q":
        clear()
        return
    else:
        error = "ERROR: The path you entered does not exist."
        message = f"{red_error}{error}{normal}\n"
    wall_selection()


def restore_default():
    global message
    Red()
    choice = input(f"""{green}
            This section allows you to reset all the settings to default.
            Note that this cannot be undone. \n{normal}
            You sure you want to continue?\n
            {green} 1: Yes {normal} \n
            {red} 2: No {normal}\n
            >>> """)
    if choice == "2":
        main_settings()
        return
    elif choice == "1":
        config.set('settings', 'download_dir',
                   os.path.join(os.environ.get("HOME"), "Pictures", "Redpaper")
                   )
        config.set('settings', 'Wallpaper_selection_method', "sequential")
        config.set('settings', 'download_limit', "1")
        set_settings()
    else:
        error = "ERROR: Choice was not understood"
        message = f"{red_error}{error}{normal}\n"
        restore_default()
        return


def main_settings():
    global message
    Red()
    choice = input(f"""{green}
            Welcome to redpaper settings menu.
            Choose an option:\n{normal}
            {red} 1 {normal}: {blue} Change download location{normal} \n
            {red} 2 {normal}: {blue} Change wallpaper selection method
            {normal}
            {red} 3 {normal}: {blue} Change the download limit{normal}\n
            {red} r {normal}: {blue} Reset to default {normal}\n
            {red} q {normal}: {blue} Quit {normal}\n
            >>>  """)
    if choice == "1":
        change_path()
    if choice == "2":
        wall_selection()
    elif choice == "3":
        max_dl_choice()
    elif choice == "r" or choice == "R":
        restore_default()
        main_settings()
    elif choice == "q" or choice == "Q":
        clear()
    if choice == "1":
        change_path()
    if choice == "2":
        wall_selection()
    elif choice == "3":
        max_dl_choice()
    elif choice == "4":
        change_subreddit()
    elif choice == "r" or choice == "R":
        restore_default()
        main_settings()
    elif choice == "x" or choice == "X":
        clear()
