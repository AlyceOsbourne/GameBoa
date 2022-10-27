import zipfile
from pathlib import Path

from project.src.system.event_handler import EventHandler
from project.src.system.events import GuiEvents, SystemEvents


@EventHandler.subscriber(GuiEvents.LoadRomFromlibrary)
def load_rom_data(file:Path):
    if file.suffix == ".zip":
        with zipfile.ZipFile(file, 'r') as z:
            for name in z.namelist():
                if name.endswith(".gb") or name.endswith(".gbc"):
                    file = z.open(name)
                    rom_data = file.read()
    else:
        with open(file, "rb") as rom_file:
            rom_data = rom_file.read()
    EventHandler.publish(SystemEvents.RomLoaded, rom_data)