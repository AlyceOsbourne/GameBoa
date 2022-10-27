from pathlib import Path
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from project.src.system.config import get_value
from project.src.system.event_handler import EventHandler
from project.src.system.events import GuiEvents, SystemEvents, ComponentEvents

rom_path = Path(get_value("paths", "roms"))


class RomLibrary(Frame):
    rom_list: Listbox
    load_button: Button
    delete_button: Button
    update_rom_list_button: Button

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
        self.delete_button = Button(self, text="Delete", command=self.delete_rom)
        self.update_rom_list_button = Button(self, text="Refresh", command=self.refresh_roms)
        # paack buttons side by side
        self.load_button.pack(side=LEFT)
        self.delete_button.pack(side=LEFT)
        self.update_rom_list_button.pack(side=LEFT)

        self.refresh_roms()

    def refresh_roms(self):
        self.roms = [rom for rom in filter(lambda p: p.suffix in {".gb", '.gbc', '.zip'}, rom_path.rglob("*"))]
        self.update_rom_list()

    def update_rom_list(self):
        self.rom_list.delete(0, END)
        for rom in self.roms:
            self.rom_list.insert(END, rom.name)

    def load_rom(self):
        if self.rom_list.curselection():
            rom = self.roms[self.rom_list.curselection()[0]]
            EventHandler.publish(GuiEvents.LoadRomFromLibrary, rom)

    def delete_rom(self):# add confirmation
        if messagebox.askyesno("Delete rom", "Are you sure you want to delete this rom?"):
            rom = self.roms[self.rom_list.curselection()[0]]
            rom.unlink()
            self.refresh_roms()





