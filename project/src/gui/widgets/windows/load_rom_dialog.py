from tkinter import filedialog

from project.src.system import data_distributor as dd
from project.src.system.config import get_value


@dd.subscribes_to(dd.GuiEvents.OpenLoadRomDialog)
def open_load_rom_dialog():
    file = filedialog.askopenfilename(
        initialdir=get_value("paths", "roms"),
        title="Load ROM file",
        filetypes=(
            ("All files", "*.gb *.gbc *.zip"),
            ("Game Boy Classic", "*.gb"),
            ("Game Boy Color", "*.gbc"),
            ("ZIP file", "*.zip"),
        ),
    )

    if file:
        dd.broadcast(dd.GuiEvents.LoadRomFromLibrary, file)
