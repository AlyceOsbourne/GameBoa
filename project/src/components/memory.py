from array import array

from project.src.system.observer import Observer
from project.src.system.event_handler import EventHandler
from project.src.system.events import ComponentEvents, GuiEvents, SystemEvents


IE: array = array("B", [0] * 1)
IO: array = array("B", [0] * 128)
OAM: array = array("B", [0] * 160)
HRAM: array = array("B", [0] * 127)
VRAM: array = array("B", [0] * 8192)
WRAM: array = array("B", [0] * 8192)
