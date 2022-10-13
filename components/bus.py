from components import system_mappings
from protocols import *


class Bus:
    """The main bus, this handles the data throughput of the gameboy"""
    __slots__ = ('ppu', 'timer', 'register', 'cpu', 'wram', 'hram', 'cart')

    def __init__(
            self,
            ppu: PPU,
            register: Register,
            wram: Bank,
            hram: Bank,
            cpu: CPU, cart: Cartridge | None = None):
        self.cart = cart
        self.ppu = ppu
        self.register = register
        self.cpu = cpu
        self.wram = wram
        self.hram = hram

    def fetch8(self) -> int:
        """Fetches 8 bits from the current PC"""
        value = self.read_address(self.read('PC'))
        self.register.write('PC', self.read('PC') + 1)
        return value

    def fetch16(self) -> int:
        """Fetches 16 bits from the current PC"""
        value = self.read_address(self.read('PC'), 2)
        self.register.write('PC', self.read('PC') + 2)
        return value

    def read(self, operator: str) -> int | bool | None:
        # gets the data based upon pattern matching
        match operator:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                """just a number"""
                return int(operator)
            case 'd16' | 'a16':
                """16 bit immediate value"""
                return self.read_address(self.read('PC'), 2)
            case 'd8' | 'a8' | 'r8':
                """8 bit signed value"""
                return self.read_address(self.read('PC'))
            case 'PC' | 'SP' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'H' | 'L' | 'AF' | 'BC' | 'DE' | 'HL':
                """Registers"""
                return self.register.read(operator)
            case '(BC)' | '(DE)' | '(HL)' | '(C)' | '(a16)' | '(a8)':
                """At address from location"""
                return self.read_address(self.read(operator[1:-1]))
            case 'HL+' | 'HL-':
                """Increment/decrement HL"""
                value = self.read('HL')
                self.register.write('HL', self.read('HL') + 1 if operator == 'HL+' else -1)
                return value
            case '(HL+)' | '(HL-)':
                """At address from location, and increment/decrement HL"""
                return self.read_address(self.read(operator[1:-1]), 1)
            case 'SP+r8':
                """SP + 8 bit immediate value"""
                return self.register.read('SP') + self.read('d8')
            case 'Z':
                """Zero flag"""
                return self.register.read('F') & 0b10000000
            case 'NZ':
                """Not zero flag"""
                return not self.register.read('F') & 0b10000000
            case 'NC':
                """Not carry flag"""
                return not self.register.read('F') & 0b00010000
            case None:
                return None
            case _:
                print(f'Unimplemented read from operator {operator}')
                return None

    def write(self, operator: str, value: any):
        match operator:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15':
                """Sets bit register r"""
                self.register.write('F', self.register.read('F') | (1 << int(operator)))
            case 'PC' | 'SP' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'H' | 'L' | 'AF' | 'BC' | 'DE' | 'HL':
                """Registers"""
                self.register.write(operator, value)
            case '(BC)' | '(DE)' | '(HL)' | '(C)' | '(a16)' | '(a8)' | '(HL+)' | '(HL-)':
                """At address from location"""
                self.write_address(self.read(operator[1:-1]), value)
            case 'd8':
                """8 bit immediate value"""
                self.write_address(self.read('PC'), value)
            case _:
                print(f'Unimplemented write to operator {operator}')

    def read_address(self, address: int, length: int = 1):
        """Reads from the address"""
        match address:
            case system_mappings.MemoryMapRanges.CARTRIDGE:
                """Cartridge"""
                return self.cart.read(address - system_mappings.MemoryMapRanges.CARTRIDGE.start, length)
            case system_mappings.MemoryMapRanges.VRAM:
                """Video RAM"""
                return self.ppu.read(address - system_mappings.MemoryMapRanges.VRAM.start, length)
            case system_mappings.MemoryMapRanges.EXT_RAM:
                """External RAM"""
                return self.cart.read(address - system_mappings.MemoryMapRanges.SRAM.start, length)
            case system_mappings.MemoryMapRanges.WRAM:
                """Work RAM"""
                return self.wram.read(address - system_mappings.MemoryMapRanges.WRAM.start, length)
            case system_mappings.MemoryMapRanges.OAM_RAM:
                """Object Attribute Memory"""
                return self.ppu.read(address - system_mappings.MemoryMapRanges.OAM.start, length)
            case system_mappings.MemoryMapRanges.ECHO_RAM:
                """Echo RAM"""
                return self.wram.read(address - system_mappings.MemoryMapRanges.ECHO.start, length)
            case system_mappings.MemoryMapRanges.UNUSED:
                """Unusable"""
                return 0xFF
            case system_mappings.MemoryMapRanges.HRAM:
                """High RAM"""
                return self.hram.read(address - system_mappings.MemoryMapRanges.HRAM.start, length)
            case system_mappings.MemoryMapRanges.IE:
                """Interrupt Enable Register"""
                return self.cpu.interrupts_enabled
            case _:
                print(
                    f'Unimplemented read from address {address}, matching ranges {system_mappings.MemoryMapRanges.from_address(address)}')
                return 0xFF

    def write_address(self, address: int, value: int):
        match address:
            case _:
                print(
                    f'Unimplemented write to address {address}, matching ranges {system_mappings.MemoryMapRanges.from_address(address)}')

    # coroutine for communication with the CPU, PPU, and APU
    def run(self):
        cpu_coro = self.cpu.run(self)
        next(cpu_coro)
        while True:
            cpu_data = cpu_coro.send(self.fetch8())

    def __str__(self):
        return f'Bus'
