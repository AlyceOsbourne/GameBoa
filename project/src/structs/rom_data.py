import zipfile
from pathlib import Path
from tkinter import messagebox

from project.src.system import ComponentEvents, EventHandler, GuiEvents, SystemEvents


@EventHandler.subscriber(GuiEvents.LoadRomFromLibrary)
def load_rom_data(file: Path | str):
    allowed_suffixes = (".gb", ".gbc", ".zip")

    if not isinstance(file, Path) and isinstance(file, str):
        file = Path(file)

    if not file.exists():
        raise FileNotFoundError(f"File {file} does not exist.")

    file_suffix = file.suffix.lower()

    if file_suffix not in allowed_suffixes:
        raise ValueError(f"File {file} is not a valid ROM file.")

    if file.suffix == ".zip":
        with zipfile.ZipFile(file) as zip_file:
            for name in zip_file.namelist():
                if name.endswith(allowed_suffixes):
                    file_contents = zip_file.open(name)
                    rom_data = file_contents.read()
                    break
            else:
                raise ValueError("No valid ROM file found in ZIP file.")
    else:
        with open(file, "rb") as rom_file:
            rom_data = rom_file.read()

    EventHandler.publish(ComponentEvents.RomLoaded, rom_data)


@EventHandler.subscriber(GuiEvents.DeleteRomFromLibrary)
def delete_rom(file_path: Path | str):
    if not isinstance(file_path, Path) and isinstance(file_path, str):
        rom_file_path = Path(file_path)

    if not rom_file_path.exists():
        raise FileNotFoundError(f"ROM file {file_path} does not exist.")

    if messagebox.askyesno("Confirmation", f"Are you sure to delete {file_path}?"):
        rom_file_path.unlink()
        EventHandler.publish(GuiEvents.UpdateRomLibrary)
