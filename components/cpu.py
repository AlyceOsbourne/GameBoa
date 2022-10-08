# gameboy cpu
import operator
from dataclasses import dataclass
import constants
from components.cartridge import Cartridge


class Decoder:
    instructions, cb_instructions = constants.Instruction.load_instructions().values()

    def decode(self, opcode, cb=False):
        return self.instructions[opcode]


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


@dataclass
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

    def read(self, address: int):
        return self.data[address]

    def write(self, address: int, value: int):
        self.data[address] = value

    @classmethod
    def of_len(cls, length: int):
        return cls(bytearray(length))


class MMU:

    def read_address(self, address, length=1):
        raise NotImplementedError

    def write_address(self, address, value):
        raise NotImplementedError


class PPU:
    tile_data: None
    tile_map: None
    oam: None


class CPU:
    def fetch(self):
        raise NotImplementedError('fetch not implemented')

    def fetch16(self):
        return self.fetch() | (self.fetch() << 8)

    def decode(self):
        raise NotImplementedError('decode not implemented')

    def execute(self):
        raise NotImplementedError('execute not implemented')


class Bus:
    cart: Cartridge
    ppu: PPU
    mmu: MMU
    timer: Timer
    regiser: Register
    cpu: CPU
