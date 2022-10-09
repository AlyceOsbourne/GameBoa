from bus.memory_bank import Bank

from bus.cartridge import Cartridge
from bus.cpu import CPU

from bus.memory_bank import Bank
from bus.cpu.cpu_register import Register
from bus.cpu.cpu_timer import Timer
from bus.memory_management_unit import MMU
from bus.picture_processing_unit import PPU


class Bus:
    cart: Cartridge | None
    ppu: PPU
    mmu: MMU
    timer: Timer
    regiser: Register
    cpu: CPU

    # all communication happens through the bus,
    # the CPU wants something from memory,
    # it calls through the bus,

    def read_operator(self, operator: str) -> int | bool:
        # gets the data based upon pattern matching
        match operator:
            case _:
                print(f'Unimplemented read from operator {operator}')

    def write_operator(self, operator: str, value: any) -> bool:
        # writes to th location based on pattern matching
        match operator:
            case _:
                print(f'Unimplemented write to operator {operator}')

    


