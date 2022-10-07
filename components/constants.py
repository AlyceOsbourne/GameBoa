import json
import logging
from collections import namedtuple
from enum import Enum, Flag

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

rom_bank_size = 0x4000
ram_bank_size = 0x2000

old_licensee_codes = {
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
}
new_licensee_codes = {
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
}
cartridge_types = {
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

}

cpu_clock_speed = 4194304
cpu_clock_speed_mhz = cpu_clock_speed / 1000000
cpu_clock_speed_mhz = round(cpu_clock_speed_mhz, 2)


class MemoryMapRanges(namedtuple(
    'MemoryMapRanges',
    'start end'
), Enum):
    ROM = 0x0000, 0x7FFF
    VRAM = 0x8000, 0x9FFF
    ERAM = 0xA000, 0xBFFF
    WRAM = 0xC000, 0xDFFF
    PPU = 0xFF00, 0xFF7F
    ECHO = 0xE000, 0xFDFF
    OAM = 0xFE00, 0xFE9F
    UNUSED = 0xFEA0, 0xFEFF
    IO = 0xFF00, 0xFF7F
    HRAM = 0xFF80, 0xFFFE
    IE = 0xFFFF, 0xFFFF
    IF = 0xFF0F, 0xFF0F

    def __contains__(self, item):
        is_in_range = self.start <= item <= self.end
        return is_in_range

    def __eq__(self, other):
        if isinstance(other, int):
            return other in self
        return super().__eq__(other)

    def __len__(self):
        return self.end - self.start + 1


class Instruction(
    namedtuple(
        'Instruction',
        'op_code mnemonic length cycles flags addr group operand1 operand2'
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
                    op_code_settings.get('mnemonic'),
                    op_code_settings.get('length'),
                    op_code_settings.get('cycles'),
                    op_code_settings.get('flags'),
                    op_code_settings.get('addr'),
                    op_code_settings.get('group'),
                    op_code_settings.get('operand1', None),
                    op_code_settings.get('operand2', None)
                )
        logger.debug(
            f'Loaded {sum([len(instructions) for instructions in loaded_instructions.values()])} instructions')
        return loaded_instructions


class Flags(Flag):
    Z = 0b10000000
    N = 0b01000000
    H = 0b00100000
    C = 0b00010000

    def __str__(self):
        return f'Z: {self.Z}, N: {self.N}, H: {self.H}, C: {self.C}'