import sys
from pathlib import Path

from .event_handler import EventHandler
from .events import SystemEvents, GuiEvents, ComponentEvents
from .config import load_config, get_value, set_value, save_config


if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    resources = Path(getattr(sys, '_MEIPASS')) / "resources"
else:
    resources = Path("project") / "resources"

opcode_path = resources / "ops.bin"
ico_path = resources / "gui" / "icons" / "icon.ico"
png_path = resources / "gui" / "icons" / "icon.png"


