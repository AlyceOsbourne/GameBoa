import os
import sys
from pathlib import Path

from .event_handler import EventHandler
from .events import SystemEvents, GuiEvents, ComponentEvents
from .config import load_config, get_value, set_value, save_config


if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    opcode_path = Path(sys._MEIPASS) / "resources" / "ops.bin"
    ico_path = Path(sys._MEIPASS) / "resources" / "gui" / "icons" / "icon.ico"
    png_path = Path(sys._MEIPASS) / "resources" / "gui" / "icons" / "icon.png"
    os.chmod(opcode_path, 0o777)
else:
    opcode_path = Path("project") / "resources" / "ops.bin"
    ico_path = Path("project") / "resources" / "gui" / "icons" / "icon.ico"
    png_path = Path("project") / "resources" / "gui" / "icons" / "icon.png"
