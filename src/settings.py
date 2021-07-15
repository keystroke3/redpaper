import os
import platform
from os.path import join
from utils import (
    colors,
    clear,
    refresh,
    message,
    settings_file,
    working_dir,
    HOME,
    parse_subs,
    get_config,
    pictures,
)


system = platform.system()
start_path = os.getcwd()
config = get_config()


class Settings:
    def main_settings(self):
        refresh(message)
        choice = input(
            f"""{colors['green']}
                Welcome to redpaper settings menu.
                Choose an option:\n{colors['normal']}
                {colors['red']} 1 {colors['normal']}: {colors['blue']} Change download location{colors['normal']} \n
                {colors['red']} 2 {colors['normal']}: {colors['blue']} Change the download limit{colors['normal']}\n
                {colors['red']} 3 {colors['normal']}: {colors['blue']} Change the source subreddits{colors['normal']}\n
                {colors['red']} r {colors['normal']}: {colors['blue']} Reset to default {colors['normal']}\n
                {colors['red']} q {colors['normal']}: {colors['blue']} Quit {colors['normal']}\n
                >>>  """
        )
        if choice == "1":
            self.change_dl_path()
        if choice == "2":
            self.max_dl_choice()
        if choice == "3":
            self.change_subs()
        elif choice == "r" or choice == "R":
            self.restore_default()
            self.main_settings()
        elif choice == "q" or choice == "Q":
            clear()

    def save_settings(self):
        """
        Writes the changed settings to file.
        """
        try:
            with open(settings_file, "w") as configfile:
                config.write(configfile)
                message = (
                    f"{colors['green']} Changes made successfully{colors['normal']}\n"
                )
                print(message)
        except FileNotFoundError:
            os.mkdir(working_dir)
            with open(settings_file, "w") as f:
                f.write("")
            Settings().save_settings()

    def change_subs(self, subs_list="", silent=False):
        """
        Allows the user to select a max number of wallpaper download attemts
        """

        if not silent:
            refresh(message)
            subs_list = input(
                f"""{colors['green']}
                Enter the subreddits you want seperated by space or comma
                e.g. wallpaper wallpapers or wallpaper,wallpapers
                {colors['normal']}\n
                {colors['red']}x{colors['normal']}: {colors['blue']} main menu{colors['normal']}
                {colors['red']}q{colors['normal']}: {colors['blue']} Quit{colors['normal']}
                >>> """
            )
        if subs_list.lower() == "x":
            self.main_settings()
            return
        elif subs_list.lower() == "q":
            clear()
        config.set("settings", "subreddits", str(parse_subs(subs_list)))
        self.save_settings()

    def max_dl_choice(self, d_limit="", silent=False, message=message):
        """
        Allows the user to select a max number of wallpaper download attemts
        """

        if not silent:
            refresh(message)
            d_limit = input(
                f"""{colors['green']}
                Enter the maximum number of wallpaper to attemt to download
                The number cannot exceed 100.
                Current value is {d_limit}
                {colors['normal']}\n
                {colors['red']}x{colors['normal']}: {colors['blue']} main menu{colors['normal']}
                {colors['red']}q{colors['normal']}: {colors['blue']} Quit{colors['normal']}
                >>> """
            )
        try:
            max_dl = int(d_limit)
            if max_dl > 100:
                message = f"{colors['green']}Please enter a value (1 - 100){colors['normal']}\n"
                print(message)
            else:
                config.set("settings", "download_limit", str(max_dl))
                self.save_settings()
        except TypeError:
            max_dl = str(d_limit)
            if max_dl == "x" or max_dl == "X":
                self.main_settings()
                return
            else:
                error = "You did not enter a number"
                message = f"{colors['red_error']}{error}{colors['normal']}\n"
                refresh(message)
                self.max_dl_choice()

    def change_dl_path(self, new_path="", silent=False, message=message):
        """
        Changes the img_path for new wallpaper downloads
        """
        if not new_path:

            refresh(message)
            new_path = input(
                f"""
                            {colors['green']}Enter the complete img_path to the new location.
                            This is case sensivite. "Pics" and "pics" are different
                            e.g. /home/user/Pictures\n
                            Current img_path is: {pictures}\n{colors['normal']}
                            {colors['red']}x{colors['normal']} : {colors['blue']}main settings{colors['normal']}
                            {colors['red']}q{colors['normal']}: {colors['blue']} Quit{colors['normal']}
                            >>> """
            )
        if new_path == "x":
            self.main_settings()
            return
        elif new_path == "q" or new_path == "Q":
            clear()
            return
        elif not os.path.exists(new_path):
            error = "ERROR: The img_path you entered does not exist."
            message = f"{colors['red_error']}{error}{colors['normal']}\n"
        else:
            config.set("settings", "download_dir", str(new_path))
            Settings().save_settings()
            message = "Path changed successfully"
            print(message)
            self.change_dl_path()

    def restore_default(self, message=message):
        refresh(message)
        choice = input(
            f"""{colors['green']}
                This section allows you to reset all the settings to default.
                Note that this cannot be undone. \n{colors['normal']}
                You sure you want to continue?\n
                {colors['green']} 1: Yes {colors['normal']} \n
                {colors['red']} 2: No {colors['normal']}\n
                >>> """
        )
        if choice == "2":
            self.main_settings()
            return
        elif choice == "1":
            config.set("settings", "download_dir", join(HOME, "Pictures", "Redpaper"))
            config.set("settings", "download_limit", "5")
            config.set("settings", "subreddits", "wallpaper+wallpapers")
            self.save_settings()
        else:
            error = "ERROR: Choice was not understood"
            message = f"{colors['red_error']}{error}{colors['normal']}\n"
            self.restore_default()
            return
