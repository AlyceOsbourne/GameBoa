from tkinter import filedialog

from project.src.system import bus as dd, GuiEvents
from project.src.system.config import get_value


@GuiEvents.OpenLoadRomDialog
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
        GuiEvents.LoadRomFromLibrary(file)
