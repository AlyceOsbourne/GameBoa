import sys
from pathlib import Path

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    resources = Path(getattr(sys, '_MEIPASS')) / "resources"
else:
    resources = Path("project") / "resources"

opcode_path = resources / "ops.bin"
ico_path = resources / "gui" / "icons" / "icon.ico"
png_path = resources / "gui" / "icons" / "icon.png"

__all__ = [
    'resources',
    'opcode_path',
    'ico_path',
    'png_path',
]