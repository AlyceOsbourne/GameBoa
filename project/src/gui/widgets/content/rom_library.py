from pathlib import Path
from tkinter import *
from tkinter.ttk import *
from project.src.system.config import get_value
from project.src.system.event_handler import EventHandler
from project.src.system.events import GuiEvents, SystemEvents, ComponentEvents
# a list that reads the filenames of the files in a directory and allows us to select them to load

rom_path = Path(get_value("paths", "roms"))

# we have a list of rom paths, a button to load them, and a botton to delete rhem as entries in the list
# this is a list of Frame objects, each of which contains a label and a button
class RomLibrary(Frame):
    rom_list: Listbox
    load_button: Button
    delete_button: Button

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=BOTH, expand=True)
        self.roms = []
        self.rom_frames = []
        self.make_widgets()

    def make_widgets(self):
        self.rom_list = Listbox(self)
        self.rom_list.pack(fill=BOTH, expand=True)
        self.load_button = Button(self, text="Load", command=self.load_rom)
        self.load_button.pack(fill=X)
        self.delete_button = Button(self, text="Delete", command=self.delete_rom)
        self.delete_button.pack(fill=X)
        self.refresh_roms()

    def refresh_roms(self):
        self.roms = [rom for rom in filter(lambda p: p.suffix in {".gb", '.gbc', '.zip'}, rom_path.rglob("*"))]
        self.update_rom_list()

    def update_rom_list(self):
        self.rom_list.delete(0, END)
        for rom in self.roms:
            self.rom_list.insert(END, rom.name)

    def load_rom(self):
        rom = self.roms[self.rom_list.curselection()[0]]
        EventHandler.publish(GuiEvents.LoadRomFromlibrary, rom)

    def delete_rom(self):
        rom = self.roms[self.rom_list.curselection()[0]]
        rom.unlink()
        self.refresh_roms()




