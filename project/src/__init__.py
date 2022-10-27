from .gui import MainWindow
from .system import EventHandler, SystemEvents, GuiEvents, ComponentEvents
from .components import *

register = Register()
mmu = MemoryManagementUnit()
cpu = CPU()
timer = Timer()
interrupts = Interrupts()
ppu = PixelProcessingUnit()
joypad = Joypad()

