import json
from enum import Enum, Flag, auto, unique
from functools import cache
from types import MappingProxyType
from typing import NamedTuple, Optional


class ScreenSize(
    NamedTuple(
        'ScreenSize',
        [
            ('width', int),
            ('height', int),
            ('tile_width', int),
            ('tile_height', int)
        ]),
    Enum
):
    """Screen size constants."""
    CLASSIC_GB = 160, 144, 20, 18
    SUPER_GB = 256, 224, 32, 28
    CLASSIC_GBC = 160, 144, 20, 18
    SUPER_GBC = 256, 224, 32, 28


class Palette(
    NamedTuple(
        'Palette',
        [('white', int), ('light_gray', int), ('dark_gray', int), ('black', int)]),
    Enum
):
    """Palette constants."""
    CLASSIC = 0xFF, 0xAA, 0x55, 0x00
    SUPER = 0xFF, 0x88, 0x44, 0x00
    POCKET = 0xFF, 0x77, 0x33, 0x00


class MemoryRange(NamedTuple(
    'MemoryRange', [('start', int), ('end', Optional[int])]
)):
    """Defines a memory range to be checked against. Is used for mappinga"""

    def __new__(cls, start: int, end: Optional[int] = None):
        return super().__new__(cls, start, end)

    def __sizeof__(self):
        return self.end - self.start + 1


class MemoryRangeEnum(MemoryRange, Enum):
    def __contains__(self, item):
        if self.end is not None:
            is_in_range = self.start <= item <= self.end
        else:
            is_in_range = self.start == item
        return is_in_range

    def __eq__(self, other):
        if isinstance(other, int):
            return other in self if self.end is not None else self.start == other
        return super().__eq__(other)

    def __len__(self):
        return self.end - self.start + 1

    @classmethod
    def to_json_tile(cls, path: str = "memory_map_ranges.json"):
        out_dict = {}
        val_fmt = "{:#06x}"
        for enum in cls:
            # for each value in the value tuple, format it if not None
            val = tuple(
                val_fmt.format(val) for val in enum.value if val is not None
            )
            out_dict[enum.name] = val
        with open(path, "w") as f:
            json.dump(out_dict, f, indent=4)

    @classmethod
    @cache
    def from_address(cls, address: int):
        matching = []
        for enum in cls:
            if address in enum:
                matching.append(enum)
        return matching


class CartridgeHeaderRanges(MemoryRangeEnum):
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


class CartridgeReadWriteRanges(MemoryRangeEnum):
    ROM_BANK_0 = 0x0000, 0x3fff
    ROM_BANK_N = 0x4000, 0x7fff
    RAM_BANK_0 = 0xa000, 0xbfff
    RAM_BANK_N = 0xa000, 0xbfff
    RAM_TIMER_ENABLE = 0x0000, 0x1fff
    ROM_BANK_SELECT = 0x2000, 0x3fff
    RAM_BANK_SELECT_OR_RTC_REGISTER_SELECT = 0x4000, 0x5fff
    LATCH_CLOCK_DATA = 0x6000, 0x7fff
    RTC_REGISTER = 0xA000, 0xBFFF


class PPUReadWriteRanges(MemoryRangeEnum):
    VRAM = 0x8000, 0x9fff
    OAM = 0xfe00, 0xfe9f
    LCDC = 0xff40
    STAT = 0xff41
    SCY = 0xff42
    SCX = 0xff43
    LY = 0xff44
    LYC = 0xff45
    DMA = 0xff46
    BGP = 0xff47
    OBP0 = 0xff48
    OBP1 = 0xff49
    WY = 0xff4a
    WX = 0xff4b

class BusReadWriteRanges(MemoryRangeEnum):
    ...




class Instruction(
    NamedTuple(
        'Instruction',
        [
            ('op_code', int),
            ('mnemonic', str),
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
    """An instruction, as defined by the Gameboy CPU"""

    @classmethod
    def load_instructions(cls, path='/op_codes.json'):
        loaded_instructions = {}
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f'Could not find {path} in the current directory.')
        for cat, ops in data.items():
            if cat not in loaded_instructions:
                loaded_instructions[cat] = {}
            for op_code, op_code_settings in ops.items():
                op_code = int(op_code, 16)
                loaded_instructions[cat][op_code] = cls(
                    op_code,
                    op_code_settings['mnemonic'],
                    op_code_settings.get('length'),
                    op_code_settings.get('cycles'),
                    op_code_settings.get('flags'),
                    op_code_settings.get('addr'),
                    op_code_settings.get('group'),
                    op_code_settings.get('operand1', None),
                    op_code_settings.get('operand2', None)
                )
        return loaded_instructions

    def __str__(self):
        return f'{self.mnemonic}({self.operand1}, {self.operand2})'


class Flags(Flag):
    """Binary flags for the CPU"""
    Z = 0b10000000
    N = 0b01000000
    H = 0b00100000
    C = 0b00010000


class Interrupts(Flag):
    """Binary interrupt flags for the CPU"""
    VBLANK = 0b00000001
    LCD_STAT = 0b00000010
    TIMER = 0b00000100
    SERIAL = 0b00001000
    JOYPAD = 0b00010000
    IF = 0b11100000



class CartType(Flag):
    ROM = auto()
    MBC1 = auto()
    MBC2 = auto()
    MBC3 = auto()
    MBC5 = auto()
    MBC6 = auto()
    MBC7 = auto()
    MMM01 = auto()
    HUC1 = auto()
    HUC3 = auto()
    POCKET_CAMERA = auto()
    BANDAI_TAMA5 = auto()
    TIMER = auto()
    BATTERY = auto()
    RUMBLE = auto()
    SENSOR = auto()
    RAM = auto()


class Model(Enum):
    DMG = auto()
    MGB = auto()
    SGB = auto()
    SGB2 = auto()
    CGB = auto()
    AGB = auto()
    AGS = auto()


ROM_BANK_SIZE = 0x4000
RAM_BANK_SIZE = 0x2000

CPU_CLOCK_SPEED = 4194304  # 4.194304 MHz
CPU_CLOCK_SPEED_MHZ = round(CPU_CLOCK_SPEED / 1000000, 2)

# immutable mappings cause ints can't be var names, and I want them as the keys here

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
    0x00: CartType.ROM,
    0x01: CartType.MBC1,
    0x02: CartType.MBC1 | CartType.RAM,
    0x03: CartType.MBC1 | CartType.RAM | CartType.BATTERY,
    0x05: CartType.MBC2,
    0x06: CartType.MBC2 | CartType.BATTERY,
    0x08: CartType.ROM | CartType.RAM,
    0x09: CartType.ROM | CartType.RAM | CartType.BATTERY,
    0x0b: CartType.MMM01,
    0x0c: CartType.MMM01 | CartType.RAM,
    0x0d: CartType.MMM01 | CartType.RAM | CartType.BATTERY,
    0x0f: CartType.MBC3 | CartType.TIMER | CartType.BATTERY,
    0x10: CartType.MBC3 | CartType.TIMER | CartType.RAM | CartType.BATTERY,
    0x11: CartType.MBC3,
    0x12: CartType.MBC3 | CartType.RAM,
    0x13: CartType.MBC3 | CartType.RAM | CartType.BATTERY,
    0x19: CartType.MBC5,
    0x1a: CartType.MBC5 | CartType.RAM,
    0x1b: CartType.MBC5 | CartType.RAM | CartType.BATTERY,
    0x1c: CartType.MBC5 | CartType.RUMBLE,
    0x1d: CartType.MBC5 | CartType.RUMBLE | CartType.RAM,
    0x1e: CartType.MBC5 | CartType.RUMBLE | CartType.RAM | CartType.BATTERY,
    0x20: CartType.MBC6,
    0x22: CartType.MBC7 | CartType.RUMBLE | CartType.RAM | CartType.BATTERY,
    0xfc: CartType.POCKET_CAMERA,
    0xfd: CartType.BANDAI_TAMA5,
    0xfe: CartType.HUC3,
    0xff: CartType.HUC1 | CartType.RAM | CartType.BATTERY,

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
NUM_RAM_BANKS = MappingProxyType({
    0x00: 0,
    0x01: 1,
    0x02: 1,
    0x03: 4,
    0x04: 16,
    0x05: 8,
})
NUM_ROM_BANKS = MappingProxyType({
    0x00: 2,
    0x01: 4,
    0x02: 8,
    0x03: 16,
    0x04: 32,
    0x05: 64,
    0x06: 128,
    0x07: 256,
    0x08: 512,
    0x52: 72,
    0x53: 80,
    0x54: 96,
})
DESTINATION_CODES = MappingProxyType({
    0x00: 'Japanese',
    0x01: 'Non-Japanese',
})
