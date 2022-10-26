import gzip
from tkinter import filedialog
from project.src.system.config import get_value
from project.src.system.event_handler import EventHandler
from project.src.system.events import GuiEvents, SystemEvents

@EventHandler.subscriber(GuiEvents.OpenLoadRomDialog)
def open_load_rom_dialog():
    file = filedialog.askopenfilename(
        initialdir=get_value("paths", "roms"),
        title="Load ROM file",
        filetypes=(
            ("Game Boy Classic", "*.gb"),
            ("Game Boy Color", "*.gbc"),
            ("ZIP file", "*.zip"),
        ),
    )

    if file:
        if file.endswith(".zip"):
            with gzip.open(file, "rb") as zip_file:
                rom_data = zip_file.read()
        else:
            with open(file, "rb") as rom_file:
                rom_data = rom_file.read()

        EventHandler.publish(SystemEvents.RomLoaded, rom_data)
