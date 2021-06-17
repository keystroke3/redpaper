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