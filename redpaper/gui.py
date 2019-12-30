#!/bin/python3
from gi.repository import Gtk, Gdk
import gi
import configparser
gi.require_version("Gtk", "3.0")


class MainWindow:
    def __init__(self):
        self.gladefile = "redpaper.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        self.dl_btn = self.builder.get_object("dl_btn")
        self.apply_btn = self.builder.get_object("apply_btn")
        self.next_btn = self.builder.get_object("next_btn")
        self.prev_btn = self.builder.get_object("prev_btn")
        self.limit_spin = self.builder.get_object("limit_spin")
        self.heart_btn = self.builder.get_object("heart_btn")
        self.heart_btn.connect("button-press-event", self.choose_file)
        self.file_chooser = self.builder.get_object("file_chooser_btn")
        self.file_chooser.connect("button-press-event", self.choose_img)
        self.img_view = self.builder.get_object("img_view")
        self.img_title = self.builder.get_object("img_title")
        self.quit_btn = self.builder.get_object("quit_btn")

        self.quit_btn.connect("button-press-event", Gtk.main_quit)
        window = self.builder.get_object("main_window")
        window.connect("delete-event", Gtk.main_quit)
        window.show_all()

    def choose_file(self):
        pass

if __name__ == "__main__":
    main = MainWindow()
    Gtk.main()
