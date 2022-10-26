import os
import pathlib
import sys
from pathlib import Path

from project.src.gui import MainWindow, open_load_rom_dialog, open_settings_dialog
from project.src.components import (
    CPU,
    Memory,
    MemoryManagementUnit,
    Joypad,
    Timer,
    Interrupts,
    Register
)
from project.src.structs.instruction import Instruction, Decoder
from project.src.system.event_handler import EventHandler
from project.src.system.events import SystemEvents, GuiEvents, ComponentEvents

if hasattr(sys, '_MEIPASS'):
    opcode_path = Path(sys._MEIPASS) / 'resources' / 'ops.bin'
    ico_path = Path(sys._MEIPASS) / 'resources' / 'gui' / 'icons' / 'icon.ico'
    os.chmod(opcode_path, 0o777)
else:
    opcode_path = Path('project') / 'resources' / 'ops.bin'
    ico_path = Path('project') / 'resources' / 'gui' / 'icons' / 'icon.ico'

main_window = MainWindow()
main_window.iconbitmap(ico_path)
decoder = Decoder(Instruction.load(Path(opcode_path)))
register = Register()
CPU = CPU()
mmu = MemoryManagementUnit()

EventHandler.subscribe(SystemEvents.Quit, sys.exit)

def main():
    main_window.show()


if __name__ == '__main__':
    main()


