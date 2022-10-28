from pathlib import Path
from tkinter import *
from tkinter.ttk import *

from project.src.system.config import get_value
from project.src.system.event_handler import EventHandler
from project.src.system.events import GuiEvents, SystemEvents

rom_path = Path(get_value("paths", "roms"))

class RomEntry(Frame):
    def __init__(self, parent, rom_path):
        super().__init__(parent)
        self.rom_path = rom_path
        self.rom_name = rom_path.name
        self.label = Label(self, text=self.rom_name)
        self.load_rom = Button(self, text="Launch", command=lambda: EventHandler.publish(GuiEvents.LoadRomFromLibrary, self.rom_path))
        self.delete_rom = Button(self, text="Delete", command=lambda: EventHandler.publish(GuiEvents.DeleteRomFromLibrary, self.rom_path))
        self.label.grid(row=0, column=0, sticky="nsew")
        self.load_rom.grid(row=0, column=1, sticky="nsew", padx=5)
        self.delete_rom.grid(row=0, column=2, sticky="nsew", padx=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)

class RomLibrary(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=BOTH, expand=True)
        self.rom_list = Frame(self)
        self.rom_list.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.update_rom_list()
        EventHandler.subscribe(GuiEvents.UpdateRomLibrary, self.update_rom_list)
        EventHandler.subscribe(SystemEvents.SettingsUpdated, self.update_rom_list)

    @staticmethod
    def refresh_roms():
        return [rom for rom in filter(lambda p: p.suffix in {".gb", '.gbc', '.zip'}, rom_path.rglob("*"))]

    def update_rom_list(self):
        for child in self.rom_list.winfo_children():
            child.destroy()
        for rom in self.refresh_roms():
            RomEntry(self.rom_list, rom).pack(fill=X)







