import gzip
from tkinter import filedialog

from src.system import EventHandler
from src.system.config import get_value
from src.system.events import SystemEvents


@EventHandler.subscriber(SystemEvents.LoadRom)
def load_rom():
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
