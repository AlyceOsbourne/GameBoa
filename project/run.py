from project.src.gui import MainWindow, open_load_rom_dialog, open_settings_dialog
from project.src.components import (
    CPU,
    Memory,
    Joypad,
    Timer,
    Interrupts,
    Register
)



main_window = MainWindow()
register = Register()


def main():
    main_window.show()


if __name__ == '__main__':
    main()


