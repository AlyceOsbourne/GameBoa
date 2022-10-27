from tkinter import filedialog

from project.src.structs.rom_data import load_rom_data
from project.src.system.config import get_value
from project.src.system.event_handler import EventHandler
from project.src.system.events import GuiEvents, SystemEvents

@EventHandler.subscriber(GuiEvents.OpenLoadRomDialog)
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
        EventHandler.publish(GuiEvents.LoadRomFromLibrary, file)


