from tkinter import filedialog
from src.system import EventHandler
import gzip
from src.system.config import get_value
from src.system.events import SystemEvents

@EventHandler.subscriber(SystemEvents.LoadRom)
def load_rom():
    file = filedialog.askopenfilename(
        initialdir=get_value('paths', 'roms'),
        title="Select rom file",
        filetypes=(
            ("Gameboy", "*.gb"),
            ("Gameboy Color", "*.gbc"),
            ("Zip", "*.zip")
        ))

    if file:
        if file.endswith('.zip'):
            with gzip.open(file, 'rb') as f:
                rom = f.read()

        else:
            with open(file, 'rb') as f:
                rom = f.read()

        EventHandler.publish(SystemEvents.RomLoaded, rom)


