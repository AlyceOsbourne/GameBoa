from tkinter import *

class MenuBarWidget(Frame):
    def __init__(
            self,
            parent,
            load_rom_publisher,
            unload_rom_publisher,
            quit_program_publisher,
            open_settings_dialog_publisher,
            open_about_dialog_publisher
    ):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui(load_rom_publisher, unload_rom_publisher, quit_program_publisher, open_settings_dialog_publisher,
                     open_about_dialog_publisher)

    def init_ui(self, load_rom_publisher, unload_rom_publisher, quit_program_publisher, open_settings_dialog_publisher,
                open_about_dialog_publisher):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Rom", command=load_rom_publisher)
        file_menu.add_command(label="Unload Rom", command=unload_rom_publisher)
        file_menu.add_command(label="Exit", command=quit_program_publisher)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Settings", command=open_settings_dialog_publisher)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=open_about_dialog_publisher)
        menubar.add_cascade(label="Help", menu=help_menu)







