from components.system_mappings import CartridgeReadWriteRanges, PPUReadWriteRanges, Interrupts
from protocols import *


class Bus:
    """The main bus, this handles the data throughput of the gameboy"""
    __slots__ = ('ppu', 'timer', 'register', 'cpu', 'wram', 'hram', 'cart', 'ime')

    def __init__(
            self,
            ppu: PPU,
            register: Register,
            wram: Bank,
            hram: Bank,
            cpu: CPU,
            timer: Timer,
            cart: Cartridge | None = None):
        self.cart = cart
        self.ppu = ppu
        self.register = register
        self.cpu = cpu
        self.wram = wram
        self.hram = hram
        self.ime = False

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

    def push(self, value: int) -> None:
        """Pushes a value onto the stack"""
        self.write('SP', self.read('SP') - 2)
        self.write_address(self.read('SP'), value)

    def pop(self) -> int:
        """Pops a value from the stack"""
        value = self.read_address(self.read('SP'), 2)
        self.write('SP', self.read('SP') + 2)
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
                # Todo: once all operator are implemented, this should be a raise
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
                # Todo: once all operator are implemented, this should be a raise
                print(f'Unimplemented write to operator {operator}')

    def read_address(self, address: int, length: int = 1):
        """Reads from the address"""
        match address:
            case (
            CartridgeReadWriteRanges.ROM_BANK_0 |
            CartridgeReadWriteRanges.ROM_BANK_N |
            CartridgeReadWriteRanges.ROM_BANK_N_1
            ) if self.cart is not None:
                """Reads from the cartridge"""
                return self.cart.read(address, length)
            case (PPUReadWriteRanges.VRAM | PPUReadWriteRanges.OAM):
                """Reads from the PPU"""
                return self.ppu.read(address, length)

            case _:
                # Todo: once all operator are implemented, this should be a raise
                print(f'Unimplemented read from address {address}')
                return 0xFF

    def write_address(self, address: int, value: int):
        """Writes to the address"""
        match address:
            case (
            CartridgeReadWriteRanges.ROM_BANK_0 |
            CartridgeReadWriteRanges.ROM_BANK_N |
            CartridgeReadWriteRanges.ROM_BANK_N_1
            ) if self.cart is not None:
                """Writes to the cartridge"""
                self.cart.write(address, value)
            case (PPUReadWriteRanges.VRAM | PPUReadWriteRanges.OAM):
                """Writes to the PPU"""
                self.ppu.write(address, value)
            case _:
                # Todo: once all operator are implemented, this should be a raise
                print(f'Unimplemented write to address {address}')

    def request_interrupt(self, interrupt: int):
        """Requests an interrupt"""
        self.hram.write(0xFF0F, self.hram.read(0xFF0F, 1) | interrupt)

    def handle_interrupts(self):
        """Handles interrupts"""
        if self.ime:
            # Interrupt master enable
            interrupt = self.hram.read(0xFF0F, 1) & self.hram.read(0xFFFF, 1)
            if interrupt:
                self.ime = False
                self.hram.write(0xFF0F, self.hram.read(0xFF0F, 1) & ~interrupt)
                self.push(self.read('PC'))
                match interrupt:
                    case 0b00000001:
                        self.write('PC', 0x0040)
                    case 0b00000010:
                        self.write('PC', 0x0048)
                    case 0b00000100:
                        self.write('PC', 0x0050)
                    case 0b00001000:
                        self.write('PC', 0x0058)
                    case 0b00010000:
                        self.write('PC', 0x0060)
                    case _:
                        print(f'Unimplemented interrupt {interrupt}')
