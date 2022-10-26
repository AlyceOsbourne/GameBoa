from tkinter import *


class MenuBarWidget(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Rom", command=self.on_load_rom)
        file_menu.add_command(label="Unload Rom", command=lambda: self.on_unload_rom)
        file_menu.add_command(label="Exit", command=lambda: self.on_exit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Settings", command=lambda: self.on_settings)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: self.on_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    def on_load_rom(self):
        print("load rom")

    def on_unload_rom(self):
        print("unload rom")

    def on_exit(self):
        print("exit")

    def on_settings(self):
        print("settings")

    def on_about(self):
        print("about")




