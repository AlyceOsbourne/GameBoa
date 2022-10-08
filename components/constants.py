import json
import logging
from enum import Enum, Flag, auto
from types import MappingProxyType
from typing import NamedTuple, Optional

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
_fh = logging.FileHandler('debug.log')
_fh.setLevel(logging.DEBUG)
_ch = logging.StreamHandler()
_ch.setLevel(logging.DEBUG)
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_fh.setFormatter(_formatter)
_ch.setFormatter(_formatter)
LOGGER.addHandler(_fh)
LOGGER.addHandler(_ch)

ROM_BANK_SIZE = 0x4000
RAM_BANK_SIZE = 0x2000

OLD_LICENSEE_CODES = MappingProxyType({
        0x00: 'None',
        0x01: 'Nintendo R&D',
        0x08: 'Capcom',
        0x09: 'Hot-B',
        0x0a: 'Jaleco',
        0x0b: 'Coconuts',
        0x0c: 'Elite Systems',
        0x13: 'Electronic Arts',
        0x18: 'Hudson Soft',
        0x19: 'ITC Entertainment',
        0x1a: 'Yanoman',
        0x1d: 'Clary',
        0x1f: 'Virgin',
        0x20: 'KSS',
        0x24: 'PCM Complete',
        0x25: 'San-X',
        0x28: 'Kotobuki Systems',
        0x29: 'SETA',
        0x30: 'Infogrames',
        0x31: 'Nintendo',
        0x32: 'Bandai',
        0x33: 'GBC_GAME',
        0x34: 'Konami',
        0x35: 'Hector',
        0x38: 'Capcom',
        0x39: 'Banpresto',
        0x3c: '',
        0x3e: 'Gremlin',
        0x41: 'Ubisoft',
        0x42: 'Atlus',
        0x44: 'Malibu',
        0x46: 'Angel',
        0x47: 'Spectrum Holobyte',
        0x49: 'Irem',
        0x4a: 'Virgin',
        0x4d: 'Malibu',
        0x4f: 'U.S. Gold',
        0x50: 'Absolute',
        0x51: 'Acclaim',
        0x52: 'Activision',
        0x53: 'American Sammy Corporation',
        0x54: 'GameTek',
        0x55: 'Park Place',
        0x56: 'LJN',
        0x57: 'Matchbox',
        0x59: 'Milton Bradley',
        0x5a: 'Mindscape',
        0x5b: 'Romstar',
        0x5c: 'Naxat Soft',
        0x5d: 'Tradewest',
        0x60: 'Titus',
        0x61: 'Virgin',
        0x67: 'Ocean',
        0x69: 'Electronic Arts',
        0x6e: 'Elite Systems',
        0x6f: 'Electro Brain',
        0x70: 'Infogrames',
        0x71: 'Interplay',
        0x72: 'Broderbund',
        0x73: 'Sculptured Soft',
        0x75: 'Sales Curve',
        0x78: 'THQ',
        0x79: 'Accolade',
        0x7a: 'Triffix Entertainment',
        0x7c: 'Microprose',
        0x7f: 'Kemco',
        0x80: 'Misawa Entertainment',
        0x83: 'LOZC',
        0x86: 'Tokuma Shoten',
        0x8b: 'Bullet-Proof',
        0x8c: 'Vic Tokai',
        0x8e: 'Ape',
        0x8f: 'I\'Max',
        0x91: 'Chunsoft',
        0x92: 'Video System',
        0x93: 'Tsuburava',
        0x95: 'Varie',
        0x96: 'Yonezawa S\'pal',
        0x97: 'Kaneko',
        0x99: 'Arc',
        0x9a: 'Nihon Bussan',
        0x9b: 'Tecmo',
        0x9c: 'Imagineer',
        0x9d: 'Banpresto',
        0x9f: 'Nova',
        0xa1: 'Hori Electric',
        0xa2: 'Bandai',
        0xa4: 'Konami',
        0xa6: 'Kawada',
        0xa7: 'Takara',
        0xa9: 'Technos Japan',
        0xaa: 'Broderbund',
        0xac: 'Toei Animation',
        0xad: 'Toho',
        0xaf: 'Namco',
        0xb0: 'Acclaim',
        0xb1: 'NEXOFT',
        0xb2: 'Bandai',
        0xb4: 'Enix',
        0xb6: 'HAL',
        0xb7: 'SNK',
        0xb9: 'Pony Canyon',
        0xba: 'Culture Brain',
        0xbb: 'Sunsoft',
        0xbd: 'Sony Imagesoft',
        0xbf: 'American Sammy Corporation',
        0xc0: 'Taito',
        0xc2: 'Kemco',
        0xc3: 'Squaresoft',
        0xc4: 'Tokuma Shoten Intermedia',
        0xc5: 'Data East',
        0xc6: 'Tonkin House',
        0xc8: 'Koei',
        0xc9: 'UFL',
        0xca: 'Ultra',
        0xcb: 'Vap',
        0xcc: 'Use',
        0xcd: 'Meldac',
        0xce: 'Pony Canyon',
        0xcf: 'Angel',
        0xd0: 'Taito',
        0xd1: 'Sofel',
        0xd2: 'Quest',
        0xd3: 'Sigma Enterprises',
        0xd4: 'Ask Kodansha',
        0xd6: 'Naxat Soft ',
        0xd7: 'Copya Systems',
        0xd9: 'Banpresto',
        0xda: 'Tomy',
        0xdb: 'LJN',
        0xdd: 'NCS',
        0xde: 'Human',
        0xdf: 'Altron',
        0xe0: 'Jaleco',
        0xe1: 'Towachiki',
        0xe2: 'Yutaka',
        0xe3: 'Varie',
        0xe5: 'Epoch',
        0xe7: 'Athena',
        0xe8: 'Asmik',
        0xe9: 'Natsume',
        0xea: 'King Records',
        0xeb: 'Atlus',
        0xec: 'Epic / Sony Records',
        0xee: 'IGS',
        0xf0: 'A-Wave',
        0xf3: 'Extreme Entertainment',
        0xff: 'LJN',
    })
NEW_LICENSEE_CODES = MappingProxyType({
    0x00: 'None',
    0x01: 'Nintendo R&D',
    0x08: 'Capcom',
    0x13: 'Electronic Arts',
    0x18: 'Hudson Soft',
    0x19: 'B-AI',
    0x20: 'KSS',
    0x22: 'POW',
    0x24: 'PCM Complete',
    0x25: 'San-X',
    0x28: 'Kemco Japan',
    0x29: 'SETA',
    0x30: 'Viacom',
    0x31: 'Nintendo',
    0x32: 'Bandai',
    0x33: 'Ocean/Acclaim',
    0x34: 'Konami',
    0x35: 'Hector',
    0x37: 'Taito',
    0x38: 'Hudson',
    0x39: 'Banpresto',
    0x41: 'Ubisoft',
    0x42: 'Atlus',
    0x44: 'Malibu',
    0x46: 'Angel',
    0x47: 'Bullet-Proof',
    0x49: 'Irem.',
    0x50: 'Absolute',
    0x51: 'Acclaim',
    0x52: 'Activision',
    0x53: 'American Sammy Corporation',
    0x54: 'Konami',
    0x55: 'Hi Tech Entertainment',
    0x56: 'LJN',
    0x57: 'Matchbox',
    0x58: 'Mattel',
    0x59: 'Milton Bradley',
    0x60: 'Titus',
    0x61: 'Virgin',
    0x64: 'LucasArts',
    0x67: 'Ocean',
    0x69: 'Electronic Arts',
    0x70: 'Infogrames',
    0x71: 'Interplay',
    0x72: 'Broderbund',
    0x73: 'Sculptured',
    0x75: 'SCI',
    0x78: 'THQ',
    0x79: 'Accolade',
    0x80: 'Misawa',
    0x83: 'LOZC',
    0x86: 'Tokuma Shoten',
    0x87: 'Tsukuda Original',
    0x91: 'Chunsoft',
    0x92: 'Video System',
    0x93: 'Ocean/Acclaim',
    0x95: 'Varie',
    0x96: 'Yonezawa / S\'pal',
    0x97: 'Kaneko',
    0x99: 'Pack-In-Video',
    0xa4: 'Konami (Yu-Gi-Oh!)',
})
CARTRIDGE_TYPES = MappingProxyType({
    0x00: 'ROM',
    0x01: 'MBC1',
    0x02: 'MBC1+RAM',
    0x03: 'MBC1+RAM+BATTERY',
    0x05: 'MBC2',
    0x06: 'MBC2+BATTERY',
    0x08: 'ROM+RAM',
    0x09: 'ROM+RAM+BATTERY',
    0x0b: 'MMM01',
    0x0c: 'MMM01+RAM',
    0x0d: 'MMM01+RAM+BATTERY',
    0x0f: 'MBC3+TIMER+BATTERY',
    0x10: 'MBC3+TIMER+RAM+BATTERY',
    0x11: 'MBC3',
    0x12: 'MBC3+RAM',
    0x13: 'MBC3+RAM+BATTERY',
    0x19: 'MBC5',
    0x1a: 'MBC5+RAM',
    0x1b: 'MBC5+RAM+BATTERY',
    0x1c: 'MBC5+RUMBLE',
    0x1d: 'MBC5+RUMBLE+RAM',
    0x1e: 'MBC5+RUMBLE+RAM+BATTERY',
    0x20: 'MBC6',
    0x22: 'MBC7+SENSOR+RUMBLE+RAM+BATTERY',
    0xfc: 'POCKET CAMERA',
    0xfd: 'BANDAI TAMA5',
    0xfe: 'HuC3',
    0xff: 'HuC1+RAM+BATTERY',

})
ROM_SIZES = MappingProxyType({
    0x00: 0x8000,
    0x01: 0x10000,
    0x02: 0x20000,
    0x03: 0x40000,
    0x04: 0x80000,
    0x05: 0x100000,
    0x06: 0x200000,
    0x07: 0x400000,
    0x08: 0x800000,
    0x52: 0x120000,
    0x53: 0x140000,
    0x54: 0x180000,
})
RAM_SIZES = MappingProxyType({
    0x00: 0x0000,
    0x01: 0x0002,
    0x02: 0x0008,
    0x03: 0x0020,
    0x04: 0x0080,
    0x05: 0x0200,
})


CPU_CLOCK_SPEED = 4194304
CPU_CLOCK_SPEED_MHZ = round(CPU_CLOCK_SPEED / 1000000, 2)


class ScreenSize(
    NamedTuple('ScreenSize', [('width', int), ('height', int), ('tile_width', int), ('tile_height', int)]),
    Enum):
    CLASSIC_GB = 160, 144, 20, 18
    SUPER_GB = 256, 224, 32, 28
    CLASSIC_GBC = 160, 144, 20, 18
    SUPER_GBC = 256, 224, 32, 28


class MemoryRange(NamedTuple(
    'MemoryRange', [('start', int), ('end', Optional[int])]
)):
    def __new__(cls, start: int, end: Optional[int] = None):
        return super().__new__(cls, start, end)


class RangeMap(MemoryRange, Enum):
    def __contains__(self, item):
        is_in_range = self.start <= item <= self.end
        return is_in_range

    def __eq__(self, other):
        if isinstance(other, int):
            return other in self if self.end is not None else self.start == other
        return super().__eq__(other)

    def __len__(self):
        return self.end - self.start + 1


class CartridgeRanges(RangeMap):
    TITLE = 0x0134, 0x0143
    NEW_LICENSEE_CODE = 0x0144, 0x0145
    SGB_FLAG = 0x0146
    CGB_FLAG = 0x0143
    CARTRIDGE_TYPE = 0x0147
    ROM_SIZE = 0x0148, 0x0148
    RAM_SIZE = 0x0149, 0x0149
    DESTINATION_CODE = 0x014a
    OLD_LICENSEE_CODE = 0x014b
    MASK_ROM_VERSION = 0x014c
    HEADER_CHECKSUM = 0x014d
    GLOBAL_CHECKSUM = 0x014e, 0x014f
    ROM_BANK_0 = 0x0000, 0x3fff
    ROM_BANK_N = 0x4000, 0x7fff
    RAM_BANK_0 = 0xa000, 0xbfff
    RAM_BANK_N = 0xa000, 0xbfff


class MemoryMapRanges(RangeMap):
    RES_INT = 0x0000, 0x00FF
    CART_HEADER = 0x0100, 0x014F
    CART_BANK_0 = 0x0150, 0x3FFF
    CART_BANK_N = 0x4000, 0x7FFF

    CHAR_RAM = 0x8000, 0x97FF
    BG_RAM_1 = 0x9800, 0x9BFF
    BG_RAM_2 = 0x9C00, 0x9FFF

    CART_RAM = 0xA000, 0xBFFF
    INTERNAL_RAM_BANK_0 = 0xC000, 0xCFFF
    INTERNAL_RAM_BANK_N = 0xD000, 0xDFFF
    ECHO_RAM = 0xE000, 0xFDFF
    OAM_RAM = 0xFE00, 0xFE9F

    UNUSED = 0xFEA0, 0xFEFF
    IO_PORTS = 0xFF00, 0xFF7F
    HRAM = 0xFF80, 0xFFFE
    INT_ENABLE = 0xFFFF


class HardwareMemoryMapRanges(RangeMap):
    SCROLL_Y = 0xFF42
    SCROLL_X = 0xFF43
    LCDC = 0xFF40
    STAT = 0xFF41
    LY = 0xFF44
    LYC = 0xFF45
    DMA = 0xFF46
    BGP = 0xFF47
    OBP0 = 0xFF48
    OBP1 = 0xFF49
    WY = 0xFF4A
    WX = 0xFF4B
    KEY1 = 0xFF4D


class Operation(Enum):
    NOP = auto()
    HALT = auto()
    STOP = auto()
    DI = auto()
    EI = auto()
    ADD = auto()
    ADC = auto()
    SUB = auto()
    SBC = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    CP = auto()
    INC = auto()
    DEC = auto()
    DAA = auto()
    CPL = auto()
    CCF = auto()
    SCF = auto()
    RC = auto()
    RLC = auto()
    RRC = auto()
    RL = auto()
    RR = auto()
    SLA = auto()
    SRA = auto()
    SRL = auto()
    JP = auto()
    JR = auto()
    CALL = auto()
    RET = auto()
    RST = auto()
    LD = auto()
    PUSH = auto()
    POP = auto()
    SWAP = auto()
    BIT = auto()
    SET = auto()
    RES = auto()
    PREFIX = auto()

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name
        return super().__eq__(other)


class Instruction(
    NamedTuple(
        'Instruction',
        [
            ('op_code', int),
            ('mnemonic', Operation),
            ('length', int),
            ('cycles', int),
            ('flags', str),
            ('addr', int),
            ('group', str),
            ('operand1', str | None),
            ('operand2', str | None)
        ]
    )
):

    @classmethod
    def load_instructions(cls, path='op_codes.json'):
        logging.debug(f'Loading instructions from {path}')
        loaded_instructions = {}
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            logging.error(f'File not found: {path}')
            quit()
        for cat, ops in data.items():
            if cat not in loaded_instructions:
                loaded_instructions[cat] = {}
            for op_code, op_code_settings in ops.items():
                op_code = int(op_code, 16)
                loaded_instructions[cat][op_code] = cls(
                    op_code,
                    Operation(op_code_settings['mnemonic']),
                    op_code_settings.get('length'),
                    op_code_settings.get('cycles'),
                    op_code_settings.get('flags'),
                    op_code_settings.get('addr'),
                    op_code_settings.get('group'),
                    op_code_settings.get('operand1', None),
                    op_code_settings.get('operand2', None)
                )
        LOGGER.debug(
            f'Loaded {sum([len(instructions) for instructions in loaded_instructions.values()])} instructions')
        return loaded_instructions


class Flags(Flag):
    Z = 0b10000000
    N = 0b01000000
    H = 0b00100000
    C = 0b00010000

    def __str__(self):
        return f'Z: {self.Z}, N: {self.N}, H: {self.H}, C: {self.C}'


class Interrupts(Flag):
    VBLANK = 0b00000001
    LCD_STAT = 0b00000010
    TIMER = 0b00000100
    SERIAL = 0b00001000
    JOYPAD = 0b00010000

    def __str__(self):
        return f'VBLANK: {self.VBLANK}, LCD_STAT: {self.LCD_STAT}, TIMER: {self.TIMER}, SERIAL: {self.SERIAL}, JOYPAD: {self.JOYPAD}'
