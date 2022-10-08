# gameboy cpu
import constants
from constants import Instruction


class Timer:
    div: int = 0
    tima: int = 0
    tma: int = 0
    tac: int = 0

    def tick(self, cycles: int):
        ...

    def read(self, address: int):
        if address == 0xFF04:
            return self.div
        elif address == 0xFF05:
            return self.tima
        elif address == 0xFF06:
            return self.tma
        elif address == 0xFF07:
            return self.tac
        else:
            raise Exception(f'Invalid address {hex(address)}')

    def write(self, address: int, value: int):
        if address == 0xFF04:
            self.div = 0
        elif address == 0xFF05:
            self.tima = value
        elif address == 0xFF06:
            self.tma = value
        elif address == 0xFF07:
            self.tac = value
        else:
            raise Exception(f'Invalid address {hex(address)}')


class Register:
    a: int = 0x01
    b: int = 0x00
    c: int = 0x13
    d: int = 0x00
    e: int = 0xD8
    h: int = 0x01
    l: int = 0x4D
    f: int = 0xB0
    sp: int = 0xFFFE
    pc: int = 0x0100

    @property
    def af(self):
        return (self.a << 8) | self.f

    @af.setter
    def af(self, value):
        self.a = (value >> 8) & 0xFF
        self.f = value & 0xFF

    @property
    def bc(self):
        return (self.b << 8) | self.c

    @bc.setter
    def bc(self, value):
        self.b = (value >> 8) & 0xFF
        self.c = value & 0xFF

    @property
    def de(self):
        return (self.d << 8) | self.e

    @de.setter
    def de(self, value):
        self.d = (value >> 8) & 0xFF
        self.e = value & 0xFF

    @property
    def hl(self):
        return (self.h << 8) | self.l

    @hl.setter
    def hl(self, value):
        self.h = (value >> 8) & 0xFF
        self.l = value & 0xFF

    def __str__(self):
        out = ''
        for key, value in {
            'A': self.a,
            'B': self.b,
            'C': self.c,
            'D': self.d,
            'E': self.e,
            'H': self.h,
            'L': self.l,
            'F': self.f,
            'SP': self.sp,
            'PC': self.pc,

        }.items():
            out += f'{key}: {value:04X} '
        return out

    def read_register(self, register: str):
        if not hasattr(self, register):
            raise Exception(f'Invalid register {register}')
        return getattr(self, register.lower())

    def write_register(self, register: str, value: int):
        if not hasattr(self, register):
            raise Exception(f'Invalid register {register}')
        setattr(self, register.lower(), value)


class Flags:
    Z: int = 0
    N: int = 0
    H: int = 0
    C: int = 0

    def read_flag(self, flag: str):
        if not hasattr(self, flag):
            raise Exception(f'Invalid flag {flag}')
        return getattr(self, flag.lower())

    def read_flags(self, flags: str):
        return [self.read_flag(flag) for flag in flags]

    def write_flag(self, flag: str, value: int):
        if not hasattr(self, flag):
            raise Exception(f'Invalid flag {flag}')
        setattr(self, flag.lower(), value)

    def write_flags(self, flags: str, values: list):
        for flag, value in zip(flags, values):
            self.write_flag(flag, value)

    def __str__(self):
        out = ''
        for key, value in {
            'Z': self.Z,
            'N': self.N,
            'H': self.H,
            'C': self.C,
        }.items():
            out += f'{key}: {value} '
        return out


class Bank:
    """Holds the memory banks for the gameboy, this can be cartridge, vram, wram, etc"""
    data: bytearray

    def __init__(self, data: bytearray):
        self.data = data

    def read(self, address: int, length):
        return self.data[address:address + length]

    def write(self, address: int, value: int):
        self.data[address] = value

    @classmethod
    def of_len(cls, length: int):
        return cls(bytearray(length))


class Cartridge:
    rom_data: bytearray
    rom_bank_0: Bank
    rom_bank_n: tuple[Bank]
    ram_bank: tuple[Bank]
    ram_enabled: bool = False
    cur_rom_bank: int = 1
    cur_ram_bank: int = 0

    def __init__(self, rom_path):
        self.rom_path = rom_path
        with open(rom_path, 'rb') as rom_file:
            self.rom_data = bytearray(rom_file.read())
        self.rom_bank_0 = Bank(self.rom_data[0x0000:0x4000])
        self.rom_bank_n = tuple(Bank(self.rom_data[0x4000 * i:0x4000 * (i + 1)]) for i in range(1, self.num_rom_banks))
        self.ram_bank = tuple(Bank.of_len(0x2000) for _ in range(self.num_ram_banks))

    def _get_as_ascii(self, start, end):
        return self.rom_data[start:end].decode('ascii')

    @property
    def title(self):
        return self._get_as_ascii(*constants.CartridgeRanges.TITLE.value).strip('\0').title()

    @property
    def old_licensee_code(self):
        return constants.OLD_LICENSEE_CODES.get(self.rom_data[constants.CartridgeRanges.OLD_LICENSEE_CODE.value[0]],
                                                'Unknown').strip('\0')

    @property
    def new_licensee_code(self):
        return constants.NEW_LICENSEE_CODES.get(self.rom_data[constants.CartridgeRanges.NEW_LICENSEE_CODE.value[0]],
                                                'Unknown')

    @property
    def sgb_flag(self):
        return bool(self.rom_data[constants.CartridgeRanges.SGB_FLAG.value[0]])

    @property
    def cgb_flag(self):
        return bool(self.rom_data[constants.CartridgeRanges.CGB_FLAG.value[0]])

    @property
    def cartridge_type(self):
        return constants.CARTRIDGE_TYPES.get(
            self.rom_data[constants.CartridgeRanges.CARTRIDGE_TYPE.value[0]],
            'Unknown'
        )

    @property
    def rom_size(self):
        return constants.ROM_SIZES.get(
            self.rom_data[constants.CartridgeRanges.ROM_SIZE.value[0]],
            'Unknown'
        )

    @property
    def ram_size(self):
        return constants.RAM_SIZES.get(self.rom_data[constants.CartridgeRanges.RAM_SIZE.value[0]], 'Unknown')

    @property
    def destination_code(self):
        return constants.DESTINATION_CODES.get(self.rom_data[constants.CartridgeRanges.DESTINATION_CODE.value[0]],
                                               'Unknown')

    @property
    def num_ram_banks(self):
        return constants.NUM_RAM_BANKS.get(self.rom_data[0x149], 0)

    @property
    def num_rom_banks(self):
        return constants.NUM_ROM_BANKS.get(self.rom_data[constants.CartridgeRanges.ROM_SIZE.value[0]], 0)

    @property
    def header_checksum(self):
        return self.rom_data[constants.CartridgeRanges.HEADER_CHECKSUM.value[0]]

    @property
    def passes_header_checksum(self):
        checksum = 0
        # add all of the bytes except the checksum byte
        for byte in self.rom_data[0x134:0x14D]:
            checksum = checksum - byte - 1
        return checksum & 0xFF == self.header_checksum

    def raw(self):
        return self.rom_data

    def __str__(self):
        return f'''Title: {self.title}
Old Licensee Code: {self.old_licensee_code}
New Licensee Code: {self.new_licensee_code}
Destination Code: {self.destination_code}
Cartridge Type: {self.cartridge_type}
SGB Flag: {self.sgb_flag}
CGB Flag: {self.cgb_flag}
ROM Size: {self.rom_size}
RAM Size: {self.ram_size}
Number of RAM Banks: {self.num_ram_banks}
Number of ROM Banks: {self.num_rom_banks}
Header Checksum: {self.header_checksum}
Passes Header Checksum: {self.passes_header_checksum}'''

    def __repr__(self):
        return f'Cartridge({repr(self.rom_path)})'

    def hex_view(self):
        out = ''
        for i in range(0, len(self.rom_data), 16):
            out += f'{i:04X}  '
            for j in range(16):
                out += f'{self.rom_data[i + j]:02X} '
            out += "  "
            for j in range(16):
                out += chr(self.rom_data[i + j] if 0x20 <= self.rom_data[i + j] <= 0x7E else 0x2E)
            out += '\n'
        return out


class MMU:
    vram: Bank
    wram: Bank
    sram: Bank
    hram: Bank
    oam: Bank

    def read_address(self, address, length=1):
        match address:
            case constants.MemoryMapRanges.VRAM:
                return self.vram.read(address, length, constants.MemoryMapRanges.VRAM.value[0])
            case constants.MemoryMapRanges.WRAM:
                return self.wram.read(address, length, constants.MemoryMapRanges.WRAM.value[0])

    def write_address(self, address, value):
        match address:
            case constants.MemoryMapRanges.VRAM:
                return self.vram.write(address, value, constants.MemoryMapRanges.VRAM.value[0])


class PPU:
    ...


class CPU:

    def fetch(self, bus: 'Bus'):
        raise NotImplementedError('fetch not implemented')

    def fetch16(self, bus: 'Bus'):
        return self.fetch(bus) | (self.fetch(bus) << 8)

    def decode(self, opcode: int, cb=False):
        return getattr(self, 'cb_' if cb else '' + 'instructions')[opcode]

    def execute(self, bus: 'Bus', instruction: 'Instruction'):
        raise NotImplementedError('execute not implemented')


class Bus:
    cart: Cartridge
    ppu: PPU
    mmu: MMU
    timer: Timer
    regiser: Register
    cpu: CPU


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
