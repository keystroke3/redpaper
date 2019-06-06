import os
import platform
import ctypes
from subprocess import Popen
import random

global path
pictures = os.path.join(os.environ.get("HOME"), "Pictures", "Redpaper")
saved_walls = os.path.join(os.environ.get("HOME"), ".redpaper", "saved")
system = platform.system()

options = []


def choose_random_wall():
    """Selects a random file from all the previous downloads"""
    global path
    selected = random.choice(os.listdir(pictures))
    path = os.path.join(pictures, selected)


def choose_by_time():
    """ Chooses a random file from the recently downloaded files"""
    global path
    with open(saved_walls) as s:
        for line in s.readlines():
            options.append(line.rstrip())
    selected = random.choice(options)
    path = os.path.join(pictures, selected)


choose_by_time()


def wall_change(*popenargs, timeout=None, **kwargs):
    """Run command with arguments.  Wait for command to complete or
    timeout, then return the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    retcode = call(["ls", "-l"])
    """
    with Popen(*popenargs, **kwargs) as p:
        try:
            return p.wait(timeout=timeout)
        except:  # Including KeyboardInterrupt, wait handled that.
            p.kill()
            # We don't call p.wait() again as p.__exit__ does that for us.
            raise


def set_wallpaper():
    # TODO: create support for MacOS
    # TODO: create support for windows

    # if system == "Windows":
    #     ctypes.windll.user32.SystemParametersInfoW(
    #         0x14, 0, config.walldir + "\\wallpaper.bmp", 0x3)
    # choose_random_wall()
    if system == "Linux":
        linux_wallpaper()
    else:
        print("Sorry, you system is not supported at the moment")
    print(f"Wallpaper was set to: {path.strip(pictures)}")


def check_de(current_de, list_of_de):
    """Check if any of the strings in ``list_of_de``
     is contained in ``current_de``."""
    return any([de in current_de for de in list_of_de])


def linux_wallpaper():
    de = os.environ.get('DESKTOP_SESSION')
    try:
        if check_de(de, ["gnome", "gnome-xorg", "gnome-wayland", "unity",
                         "ubuntu", "ubuntu-xorg", "budgie-desktop"]):
            wall_change(["gsettings", "set", "org.gnome.desktop.background",
                         "picture-uri",
                         "file://%s" % path])

        elif check_de(de, ["cinnamon"]):
            wall_change(["gsettings", "set", "org.cinnamon.desktop.background",
                         "picture-uri",
                         "file://%s" % path])

        # TODO: fix this code to better support pantheon

        elif check_de(de, ["mate"]):
            wall_change(["gsettings", "set", "org.mate.background",
                         "picture-filename", "'%s'" % path])

        elif check_de(de, ["xfce", "xubuntu"]):
            # Light workaround here, just need to toggle the wallpaper
            #  from null to the original filename
            # xfconf props aren't 100% consistent so light workaround
            #  for that too
            props = check_output(['xfconf-query', '-c', 'xfce4-desktop', '-p',
                                  '/backdrop', '-l'])\
                .decode("utf-8").split('\n')
            for prop in props:
                if "last-image" in prop or "image-path" in prop:
                    wall_change(
                        ["xfconf-query", "-c", "xfce4-desktop", "-p", prop,
                         "-s", "''"])
                    wall_change(["xfconf-query", "-c", "xfce4-desktop",
                                 "-p", prop, "-s" "'%s'" % path])
                if "image-show" in prop:
                    wall_change(
                        ["xfconf-query", "-c", "xfce4-desktop", "-p", prop,
                         "-s", "'true'"])

        elif check_de(de, ["lubuntu", "Lubuntu"]):
            wall_change(["pcmanfm", "-w", "%s" % path])

        elif check_de(de, ["i3", "bspwm"]):
            wall_change(["feh", "--bg-fill", path])

        elif check_de(de, ["sway"]):
            wall_change(["swaymsg", "output * bg %s fill" % path])

        else:
            print("Your DE could not be detected to set the wallpaper. "
                  "You need to set the 'setcommand' paramter at"
                  "~/.config/wallpaper-reddit. "
                  "When you get it working, please file an issue.")
            sys.exit(1)
    except:
        print("Command to set wallpaper returned non-zero exit code."
              " Please file an issue or check your custom "
              "command if you have set one in the configuration file.")
