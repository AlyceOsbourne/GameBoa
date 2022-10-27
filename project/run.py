from sys import exit
from pathlib import Path

from project.src.system import opcode_path
from project.src.system.event_handler import EventHandler
from project.src.structs.instruction import Decoder, Instruction
from project.src.system.events import ComponentEvents, GuiEvents, SystemEvents
from project.src.gui import MainWindow, open_load_rom_dialog, open_settings_dialog
from project.src.components import (
    CPU,
    Timer,
    Joypad,
    Memory,
    Register,
    Interrupts,
    MemoryManagementUnit,
)


decoder = Decoder(Instruction.load(Path(opcode_path)))
register = Register()
CPU = CPU()
mmu = MemoryManagementUnit()

EventHandler.subscribe(SystemEvents.Quit, exit)


def main():
    main_window = MainWindow()
    main_window.show()


if __name__ == "__main__":
    main()
