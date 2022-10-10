from dataclasses import dataclass

from bus.memory_bank import Bank

from bus.cartridge import Cartridge
from bus.cpu import CPU

from bus.memory_bank import Bank
from bus.cpu.cpu_register import Register
from bus.cpu.cpu_timer import Timer
from bus.memory_management_unit import MMU
from bus.picture_processing_unit import PPU

@dataclass
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
    def __init__(self, ppu: PPU, mmu: MMU, timer: Timer, register: Register, cpu: CPU):
        self.ppu = ppu
        self.mmu = mmu
        self.timer = timer
        self.regiser = register
        self.cpu = cpu

    def read_operator(self, operator: str) -> int | bool | None:
        # gets the data based upon pattern matching
        match operator:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                """just a number"""
            case 'd16' | 'a16':
                """16 bit immediate value"""
            case 'd8' | 'a8':
                """8 bit immediate value"""
            case 'r8':
                """8 bit signed immediate value"""
            case 'PC' | 'SP' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'H' | 'L' | 'AF' | 'BC' | 'DE' | 'HL':
                """Registers"""
            case '(BC)' | '(DE)' | '(HL)' | '(C)' | '(a16)' | '(a8)':
                """At address from location"""
            case '(HL+)' | '(HL-)':
                """At address from location, and increment/decrement HL"""
            case 'SP+r8':
                """SP + 8 bit immediate value"""
            case 'Z' | 'NZ' | 'NC':
                """Condition"""
            case None:
                return None
            case _:
                print(f'Unimplemented read from operator {operator}')
                return None
        return 0

    def write_operator(self, operator: str, value: any):
        match operator:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                """Sets bit register r"""
            case 'PC' | 'SP' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'H' | 'L' | 'AF' | 'BC' | 'DE' | 'HL':
                """Registers"""
            case '(BC)' | '(DE)' | '(HL)' | '(C)'| '(a16)' | '(a8)'| '(HL+)' | '(HL-)':
                """At address from location"""
            case 'd8':
                """8 bit immediate value"""
            case _:
                print(f'Unimplemented write to operator {operator}')

    


