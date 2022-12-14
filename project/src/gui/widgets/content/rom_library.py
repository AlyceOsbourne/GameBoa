import tkinter.ttk
from pathlib import Path
from tkinter import BOTH, X

from project.src.system import bus as dd, SystemEvents, GuiEvents
from project.src.system.config import get_value

ROM_PATH = Path(get_value("paths", "roms"))


class RomEntry(tkinter.ttk.Frame):
    def __init__(self, parent, rom_path):
        super().__init__(parent)
        self.rom_path = rom_path
        self.rom_name = rom_path.name
        self.label = tkinter.ttk.Label(self, text=self.rom_name)
        self.load_rom = tkinter.ttk.Button(
            self,
            text="Launch",
            command=lambda:GuiEvents.LoadRomFromLibrary(self.rom_path)

        )
        self.delete_rom = tkinter.ttk.Button(
            self,
            text="Delete",
            command=lambda: GuiEvents.DeleteRomFromLibrary(self.rom_path)

        )
        self.label.grid(row=0, column=0, sticky="nsew")
        self.load_rom.grid(row=0, column=1, sticky="nsew", padx=5)
        self.delete_rom.grid(row=0, column=2, sticky="nsew", padx=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)


class RomLibrary(tkinter.ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=BOTH, expand=True)
        self.rom_list = tkinter.ttk.Frame(self)
        self.rom_list.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.update_rom_list()
        GuiEvents.UpdateRomLibrary(self.update_rom_list)
        SystemEvents.SettingsUpdated(self.update_rom_list)

    @staticmethod
    def refresh_roms():
        return [
            rom
            for rom in filter(
                lambda p: p.suffix in {".gb", ".gbc", ".zip"}, ROM_PATH.rglob("*")
            )
        ]

    def update_rom_list(self, *args):
        for child in self.rom_list.winfo_children():
            child.destroy()
        for rom in self.refresh_roms():
            RomEntry(self.rom_list, rom).pack(fill=X)


__all__ = ["RomLibrary"]
