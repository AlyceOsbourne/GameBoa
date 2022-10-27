import zipfile
from pathlib import Path

from project.src.system import (
    EventHandler,
    GuiEvents,
    SystemEvents,
    ComponentEvents
)


@EventHandler.subscriber(GuiEvents.LoadRomFromLibrary)
def load_rom_data(file:Path|str):
    allowed_suffixes = (".gb", ".gbc", ".zip")

    if not isinstance(file, Path) and isinstance(file, str):
        file = Path(file)

    if not file.exists():
        raise FileNotFoundError(f"File {file} does not exist.")

    file_suffix = file.suffix.lower()
    if file_suffix not in allowed_suffixes:
        raise ValueError(f"File {file} is not a valid rom file.")

    if file.suffix == ".zip":
        with zipfile.ZipFile(file) as zip_file:
            for name in zip_file.namelist():
                if name.endswith(allowed_suffixes):
                    file = zip_file.open(name)
                    rom_data = file.read()
                    break
            else:
                raise ValueError("No valid rom file found in zip file")
    else:
        with open(file, "rb") as rom_file:
            rom_data = rom_file.read()
    EventHandler.publish(ComponentEvents.RomLoaded, rom_data)