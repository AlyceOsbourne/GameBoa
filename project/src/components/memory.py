import array

from project.src.system.event_handler import EventHandler
from project.src.system.events import SystemEvents, GuiEvents, ComponentEvents


WRAM = array.array('B', [0] * 8192)
VRAM = array.array('B', [0] * 8192)
OAM = array.array('B', [0] * 160)
IO = array.array('B', [0] * 128)
HRAM = array.array('B', [0] * 127)
IE = array.array('B', [0] * 1)





