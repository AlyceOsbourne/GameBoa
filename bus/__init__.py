# gameboy cpu
from bus.cartridge import Cartridge
from bus.cpu import CPU

from bus.memory_bank import Bank
from bus.cpu_register import Register
from bus.cpu_timer import Timer
from bus.memory_bank import Bank
from bus.memory_management_unit import MMU
from bus.picture_processing_unit import PPU


class Bus:
    cart: Cartridge
    ppu: PPU
    mmu: MMU
    timer: Timer
    regiser: Register
    cpu: CPU

    def read_operator(self, operator):
        ...

    def write_operator(self, operator, value):
        ...


if __name__ == "__main__":
    rom_path = 'roms/tetris.gb'
    cart = Cartridge(rom_path)
    print(cart)

    if input('View hex view? (y/n) ') == 'y':
        print('will print in small chunks, press enter to continue')
        for i, line in enumerate(cart.hex_view().splitlines(), 1):
            print(f'{i:04X} {line}')
            if i % 100 == 0:
                input()
