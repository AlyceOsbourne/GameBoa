from tkinter import *
from project.src.system import data_distributor as dd


class MenuBarWidget(Frame):
    def __init__(
        self,
        parent,
    ):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="Load Rom",
            command=lambda: dd.broadcast(dd.GuiEvents.OpenLoadRomDialog),
        )
        file_menu.add_command(
            label="Unload Rom",
            command=lambda: dd.broadcast(dd.ComponentEvents.RequestReset),
        )
        file_menu.add_command(
            label="Exit", command=lambda: dd.broadcast(dd.SystemEvents.Quit)
        )
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(
            label="Settings",
            command=lambda: dd.broadcast(
                dd.GuiEvents.OpenSettingsDialog, self.parent
            ),
        )
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="About",
            command=lambda: dd.broadcast(
                dd.GuiEvents.OpenAboutDialog, self.parent
            ),
        )
        menubar.add_cascade(label="Help", menu=help_menu)
