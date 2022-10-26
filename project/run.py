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


decoder = Decoder(Instruction.load())
main_window = MainWindow()
register = Register()
CPU = CPU()
mmu = MemoryManagementUnit()



def main():
    main_window.show()


if __name__ == '__main__':
    main()


