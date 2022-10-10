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
    """The main bus, this handles the data throughput of the gameboy"""
    cart: Cartridge | None
    ppu: PPU
    mmu: MMU
    timer: Timer
    register: Register
    cpu: CPU

    def __init__(self, ppu: PPU, mmu: MMU, timer: Timer, register: Register, cpu: CPU):
        self.cart = None
        self.ppu = ppu
        self.mmu = mmu
        self.timer = timer
        self.register = register
        self.cpu = cpu

    def read(self, operator: str) -> int | bool | None:
        # gets the data based upon pattern matching
        match operator:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                """just a number"""
                return int(operator)
            case 'd16' | 'a16':
                """16 bit immediate value"""
                return self.mmu.read_address(self.read('PC'), 2)
            case 'd8' | 'a8' | 'r8':
                """8 bit signed value"""
                return self.mmu.read_address(self.read('PC'), 1)
            case 'PC' | 'SP' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'H' | 'L' | 'AF' | 'BC' | 'DE' | 'HL':
                """Registers"""
                return self.register.read_register(operator)
            case '(BC)' | '(DE)' | '(HL)' | '(C)' | '(a16)' | '(a8)':
                """At address from location"""
                return self.mmu.read_address(self.read(operator[1:-1]), 1)
            case '(HL+)' | '(HL-)':
                """At address from location, and increment/decrement HL"""
                value = self.mmu.read_address(self.read('HL'), 1)
                self.register.write_register('HL', self.read('HL') + 1 if operator == '(HL+)' else -1)
                return value
            case 'SP+r8':
                """SP + 8 bit immediate value"""
                return self.register.read_register('SP') + self.read('d8')
            case 'Z' | 'NZ' | 'NC':
                """Condition"""
                if operator == 'Z':
                    return self.register.read_register('F') & 0b10000000
                elif operator == 'NZ':
                    return not self.register.read_register('F') & 0b10000000
                elif operator == 'NC':
                    return not self.register.read_register('F') & 0b00010000
            case None:
                return None
            case _:
                print(f'Unimplemented read from operator {operator}')
                return None
        return 0

    def write(self, operator: str, value: any):
        match operator:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                """Sets bit register r"""
                self.register.write_register('F', self.register.read_register('F') | (1 << int(operator)))
            case 'PC' | 'SP' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'H' | 'L' | 'AF' | 'BC' | 'DE' | 'HL':
                """Registers"""
                self.register.write_register(operator, value)
            case '(BC)' | '(DE)' | '(HL)' | '(C)' | '(a16)' | '(a8)' | '(HL+)' | '(HL-)':
                """At address from location"""
                self.mmu.write_address(self.read(operator[1:-1]), value)
            case 'd8':
                """8 bit immediate value"""
                self.mmu.write_address(self.read('PC'), value)
            case _:
                print(f'Unimplemented write to operator {operator}')

    def __str__(self):
        return f'Bus'
