import json
from functools import cache
from enum import auto, Enum, Flag, IntFlag
from types import MappingProxyType
from typing import NamedTuple, Optional


class Model(Enum):
    ...


class DMGModel(Model):
    DMG = auto()
    MGB = auto()
    SGB = auto()
    CGB = auto()
    AGB = auto()
    AGS = auto()


class CGBModel(Model):
    CGB = auto()
    AGB = auto()
    AGS = auto()


class RegisterDefault(NamedTuple('RegisterDefaults', [
    ('af', int),
    ('bc', int),
    ('de', int),
    ('hl', int),
    ('sp', int),
    ('pc', int),
])):
    pass


class RegisterDefaults(RegisterDefault, Enum):
    ...


class DMGModelRegisterDefaults(RegisterDefaults):
    DMG = 0x01B0, 0x0013, 0x00D8, 0x014D, 0xFFFE, 0x0100
    MGB = 0xFFB0, 0x0013, 0x00D8, 0x014D, 0xFFFE, 0x0100
    SGB = 0x0100, 0x0014, 0x0000, 0x060C, 0xFFFE, 0x0100
    CGB = 0x1180, 0x0000, 0x0008, 0x007C, 0xFFFE, 0x0100
    AGB = 0x1100, 0x0100, 0x0008, 0x007C, 0xFFFE, 0x0100
    AGS = 0x1100, 0x0100, 0x0008, 0x007C, 0xFFFE, 0x0100


class CGBModelRegisterDefaults(RegisterDefaults):
    CGB = 0x1180, 0x0000, 0xFF56, 0x000D, 0xFFFE, 0x0100
    AGB = 0x1100, 0x0100, 0xFF56, 0x000D, 0xFFFE, 0x0100
    AGS = 0x1100, 0x0100, 0xFF56, 0x000D, 0xFFFE, 0x0100


class ScreenSize(
    NamedTuple(
        "ScreenSize",
        [("width", int), ("height", int), ("tile_width", int), ("tile_height", int)],
    ),
    Enum,
):
    """A screen size of each Game Boy edition."""

    SUPER_GB = 256, 224, 32, 28
    SUPER_GBC = 256, 224, 32, 28
    CLASSIC_GB = 160, 144, 20, 18
    CLASSIC_GBC = 160, 144, 20, 18
    ADVANCED_GB = 240, 160, 30, 20
    ADVANCED_GBC = 240, 160, 30, 20
    ADVANCED_GBS = 240, 160, 30, 20


class Palette(
    NamedTuple(
        "Palette",
        [("white", int), ("light_gray", int), ("dark_gray", int), ("black", int)],
    ),
    Enum,
):
    """Color palettes of different Game Boy editions."""

    SUPER = 0xFF, 0x88, 0x44, 0x00
    POCKET = 0xFF, 0x77, 0x33, 0x00
    CLASSIC = 0xFF, 0xAA, 0x55, 0x00


class MemoryRange(NamedTuple("MemoryRange", [("start", int), ("end", Optional[int])])):
    """A memory range to be checked against and used for mappings."""

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
    def to_json_file(cls, json_file: Optional[str] = None):
        if json_file is None:
            json_file = cls.__name__ + ".json"

        output_dictionary = {}

        for enum in cls:
            enum_value = tuple(
                f"{value:#06x}" for value in enum.value if value is not None
            )
            output_dictionary[enum.name] = enum_value

        with open(json_file, "w") as memory_map_ranges:
            json.dump(output_dictionary, memory_map_ranges, indent=2)

    @classmethod
    def from_address(cls, address: int):
        matching = []

        for enum in cls:
            if address in enum:
                matching.append(enum)

        return matching


class CartridgeHeaderRanges(MemoryRangeEnum):
    CGB_FLAG = 0x0143
    SGB_FLAG = 0x0146
    TITLE = 0x0134, 0x0143
    CARTRIDGE_TYPE = 0x0147
    HEADER_CHECKSUM = 0x014D
    DESTINATION_CODE = 0x014A
    MASK_ROM_VERSION = 0x014C
    RAM_SIZE = 0x0149, 0x0149
    ROM_SIZE = 0x0148, 0x0148
    OLD_LICENSEE_CODE = 0x014B
    GLOBAL_CHECKSUM = 0x014E, 0x014F
    NEW_LICENSEE_CODE = 0x0144, 0x0145


class CartridgeReadWriteRanges(MemoryRangeEnum):
    RAM_BANK_0 = 0xA000, 0xBFFF
    RAM_BANK_N = 0xA000, 0xBFFF
    ROM_BANK_0 = 0x0000, 0x3FFF
    ROM_BANK_N = 0x4000, 0x7FFF
    RTC_REGISTER = 0xA000, 0xBFFF
    ROM_BANK_SELECT = 0x2000, 0x3FFF
    RAM_TIMER_ENABLE = 0x0000, 0x1FFF
    LATCH_CLOCK_DATA = 0x6000, 0x7FFF
    RAM_BANK_SELECT_OR_RTC_REGISTER_SELECT = 0x4000, 0x5FFF


class PPUReadWriteRanges(MemoryRangeEnum):
    LY = 0xFF44
    WX = 0xFF4B
    WY = 0xFF4A
    BGP = 0xFF47
    DMA = 0xFF46
    LYC = 0xFF45
    SCX = 0xFF43
    SCY = 0xFF42
    LCDC = 0xFF40
    OBP0 = 0xFF48
    OBP1 = 0xFF49
    STAT = 0xFF41
    OAM = 0xFE00, 0xFE9F
    VRAM = 0x8000, 0x9FFF


class BusReadWriteRanges(MemoryRangeEnum):
    HRAM = 0xFF80, 0xFFFE
    WRAM = 0xC000, 0xDFFF
    IE = 0xFFFF
    IF = 0xFF0F


class Instruction(
    NamedTuple(
        "Instruction",
        [
            ("op_code", int),
            ("mnemonic", str),
            ("length", int),
            ("cycles", int),
            ("flags", str),
            ("addr", int),
            ("group", str),
            ("operand1", str | None),
            ("operand2", str | None),
        ],
    )
):
    """Instructions of the CPU."""

    @classmethod
    def load(cls, json_file: str = "/op_codes.json") -> dict:
        loaded_instructions: dict = {}

        try:
            with open(json_file, "r") as op_codes_file:
                json_data = json.load(op_codes_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {json_file} in current directory.")

        for category, operation in json_data.items():
            if category not in loaded_instructions:
                loaded_instructions[category] = {}

            for op_code, op_code_settings in operation.items():
                op_code = int(op_code, 16)
                loaded_instructions[category][op_code] = cls(
                    op_code,
                    op_code_settings["mnemonic"],
                    op_code_settings.get("length"),
                    op_code_settings.get("cycles"),
                    op_code_settings.get("flags"),
                    op_code_settings.get("addr"),
                    op_code_settings.get("group"),
                    op_code_settings.get("operand1", None),
                    op_code_settings.get("operand2", None),
                )

        return loaded_instructions

    def __str__(self) -> str:
        return f"{self.mnemonic}({self.operand1}, {self.operand2})"


class Flags(IntFlag):
    """Binary flags for the CPU."""
    Z = 0b10000000
    N = 0b01000000
    H = 0b00100000
    C = 0b00010000







class Interrupts(Flag):
    """Binary interrupt flags for the CPU."""
    # ordered by priority, lowest to highest

    JOYPAD = 0b00010000
    SERIAL = 0b00001000
    TIMER = 0b00000100
    LCD_STAT = 0b00000010
    VBLANK = 0b00000001

    def priority(self):
        """Orders flags by priority from the lowest to the highest."""
        return self.value.bit_length() - 1


class CartType(Flag):
    RAM = auto()
    ROM = auto()
    HUC1 = auto()
    HUC3 = auto()
    MBC1 = auto()
    MBC2 = auto()
    MBC3 = auto()
    MBC5 = auto()
    MBC6 = auto()
    MBC7 = auto()
    MMM01 = auto()
    TIMER = auto()
    RUMBLE = auto()
    SENSOR = auto()
    BATTERY = auto()
    BANDAI_TAMA5 = auto()
    POCKET_CAMERA = auto()


OLD_LICENSEE_CODES = MappingProxyType(
    {
        0x00: "None",
        0x01: "Nintendo R&D",
        0x08: "Capcom",
        0x09: "Hot-B",
        0x0A: "Jaleco",
        0x0B: "Coconuts",
        0x0C: "Elite Systems",
        0x13: "Electronic Arts",
        0x18: "Hudson Soft",
        0x19: "ITC Entertainment",
        0x1A: "Yanoman",
        0x1D: "Clary",
        0x1F: "Virgin",
        0x20: "KSS",
        0x24: "PCM Complete",
        0x25: "San-X",
        0x28: "Kotobuki Systems",
        0x29: "SETA",
        0x30: "Infogrames",
        0x31: "Nintendo",
        0x32: "Bandai",
        0x33: "GBC_GAME",
        0x34: "Konami",
        0x35: "Hector",
        0x38: "Capcom",
        0x39: "Banpresto",
        0x3C: "",
        0x3E: "Gremlin",
        0x41: "Ubisoft",
        0x42: "Atlus",
        0x44: "Malibu",
        0x46: "Angel",
        0x47: "Spectrum Holobyte",
        0x49: "Irem",
        0x4A: "Virgin",
        0x4D: "Malibu",
        0x4F: "U.S. Gold",
        0x50: "Absolute",
        0x51: "Acclaim",
        0x52: "Activision",
        0x53: "American Sammy Corporation",
        0x54: "GameTek",
        0x55: "Park Place",
        0x56: "LJN",
        0x57: "Matchbox",
        0x59: "Milton Bradley",
        0x5A: "Mindscape",
        0x5B: "Romstar",
        0x5C: "Naxat Soft",
        0x5D: "Tradewest",
        0x60: "Titus",
        0x61: "Virgin",
        0x67: "Ocean",
        0x69: "Electronic Arts",
        0x6E: "Elite Systems",
        0x6F: "Electro Brain",
        0x70: "Infogrames",
        0x71: "Interplay",
        0x72: "Broderbund",
        0x73: "Sculptured Soft",
        0x75: "Sales Curve",
        0x78: "THQ",
        0x79: "Accolade",
        0x7A: "Triffix Entertainment",
        0x7C: "Microprose",
        0x7F: "Kemco",
        0x80: "Misawa Entertainment",
        0x83: "LOZC",
        0x86: "Tokuma Shoten",
        0x8B: "Bullet-Proof",
        0x8C: "Vic Tokai",
        0x8E: "Ape",
        0x8F: "I'Max",
        0x91: "Chunsoft",
        0x92: "Video System",
        0x93: "Tsuburava",
        0x95: "Varie",
        0x96: "Yonezawa S'pal",
        0x97: "Kaneko",
        0x99: "Arc",
        0x9A: "Nihon Bussan",
        0x9B: "Tecmo",
        0x9C: "Imagineer",
        0x9D: "Banpresto",
        0x9F: "Nova",
        0xA1: "Hori Electric",
        0xA2: "Bandai",
        0xA4: "Konami",
        0xA6: "Kawada",
        0xA7: "Takara",
        0xA9: "Technos Japan",
        0xAA: "Broderbund",
        0xAC: "Toei Animation",
        0xAD: "Toho",
        0xAF: "Namco",
        0xB0: "Acclaim",
        0xB1: "NEXOFT",
        0xB2: "Bandai",
        0xB4: "Enix",
        0xB6: "HAL",
        0xB7: "SNK",
        0xB9: "Pony Canyon",
        0xBA: "Culture Brain",
        0xBB: "Sunsoft",
        0xBD: "Sony Imagesoft",
        0xBF: "American Sammy Corporation",
        0xC0: "Taito",
        0xC2: "Kemco",
        0xC3: "Squaresoft",
        0xC4: "Tokuma Shoten Intermedia",
        0xC5: "Data East",
        0xC6: "Tonkin House",
        0xC8: "Koei",
        0xC9: "UFL",
        0xCA: "Ultra",
        0xCB: "Vap",
        0xCC: "Use",
        0xCD: "Meldac",
        0xCE: "Pony Canyon",
        0xCF: "Angel",
        0xD0: "Taito",
        0xD1: "Sofel",
        0xD2: "Quest",
        0xD3: "Sigma Enterprises",
        0xD4: "Ask Kodansha",
        0xD6: "Naxat Soft ",
        0xD7: "Copya Systems",
        0xD9: "Banpresto",
        0xDA: "Tomy",
        0xDB: "LJN",
        0xDD: "NCS",
        0xDE: "Human",
        0xDF: "Altron",
        0xE0: "Jaleco",
        0xE1: "Towachiki",
        0xE2: "Yutaka",
        0xE3: "Varie",
        0xE5: "Epoch",
        0xE7: "Athena",
        0xE8: "Asmik",
        0xE9: "Natsume",
        0xEA: "King Records",
        0xEB: "Atlus",
        0xEC: "Epic / Sony Records",
        0xEE: "IGS",
        0xF0: "A-Wave",
        0xF3: "Extreme Entertainment",
        0xFF: "LJN",
    }
)
NEW_LICENSEE_CODES = MappingProxyType(
    {
        0x00: "None",
        0x01: "Nintendo R&D",
        0x08: "Capcom",
        0x13: "Electronic Arts",
        0x18: "Hudson Soft",
        0x19: "B-AI",
        0x20: "KSS",
        0x22: "POW",
        0x24: "PCM Complete",
        0x25: "San-X",
        0x28: "Kemco Japan",
        0x29: "SETA",
        0x30: "Viacom",
        0x31: "Nintendo",
        0x32: "Bandai",
        0x33: "Ocean/Acclaim",
        0x34: "Konami",
        0x35: "Hector",
        0x37: "Taito",
        0x38: "Hudson",
        0x39: "Banpresto",
        0x41: "Ubisoft",
        0x42: "Atlus",
        0x44: "Malibu",
        0x46: "Angel",
        0x47: "Bullet-Proof",
        0x49: "Irem.",
        0x50: "Absolute",
        0x51: "Acclaim",
        0x52: "Activision",
        0x53: "American Sammy Corporation",
        0x54: "Konami",
        0x55: "Hi Tech Entertainment",
        0x56: "LJN",
        0x57: "Matchbox",
        0x58: "Mattel",
        0x59: "Milton Bradley",
        0x60: "Titus",
        0x61: "Virgin",
        0x64: "LucasArts",
        0x67: "Ocean",
        0x69: "Electronic Arts",
        0x70: "Infogrames",
        0x71: "Interplay",
        0x72: "Broderbund",
        0x73: "Sculptured",
        0x75: "SCI",
        0x78: "THQ",
        0x79: "Accolade",
        0x80: "Misawa",
        0x83: "LOZC",
        0x86: "Tokuma Shoten",
        0x87: "Tsukuda Original",
        0x91: "Chunsoft",
        0x92: "Video System",
        0x93: "Ocean/Acclaim",
        0x95: "Varie",
        0x96: "Yonezawa / S'pal",
        0x97: "Kaneko",
        0x99: "Pack-In-Video",
        0xA4: "Konami (Yu-Gi-Oh!)",
    }
)
CARTRIDGE_TYPES = MappingProxyType(
    {
        0x00: CartType.ROM,
        0x01: CartType.MBC1,
        0x02: CartType.MBC1 | CartType.RAM,
        0x03: CartType.MBC1 | CartType.RAM | CartType.BATTERY,
        0x05: CartType.MBC2,
        0x06: CartType.MBC2 | CartType.BATTERY,
        0x08: CartType.ROM | CartType.RAM,
        0x09: CartType.ROM | CartType.RAM | CartType.BATTERY,
        0x0B: CartType.MMM01,
        0x0C: CartType.MMM01 | CartType.RAM,
        0x0D: CartType.MMM01 | CartType.RAM | CartType.BATTERY,
        0x0F: CartType.MBC3 | CartType.TIMER | CartType.BATTERY,
        0x10: CartType.MBC3 | CartType.TIMER | CartType.RAM | CartType.BATTERY,
        0x11: CartType.MBC3,
        0x12: CartType.MBC3 | CartType.RAM,
        0x13: CartType.MBC3 | CartType.RAM | CartType.BATTERY,
        0x19: CartType.MBC5,
        0x1A: CartType.MBC5 | CartType.RAM,
        0x1B: CartType.MBC5 | CartType.RAM | CartType.BATTERY,
        0x1C: CartType.MBC5 | CartType.RUMBLE,
        0x1D: CartType.MBC5 | CartType.RUMBLE | CartType.RAM,
        0x1E: CartType.MBC5 | CartType.RUMBLE | CartType.RAM | CartType.BATTERY,
        0x20: CartType.MBC6,
        0x22: CartType.MBC7 | CartType.RUMBLE | CartType.RAM | CartType.BATTERY,
        0xFC: CartType.POCKET_CAMERA,
        0xFD: CartType.BANDAI_TAMA5,
        0xFE: CartType.HUC3,
        0xFF: CartType.HUC1 | CartType.RAM | CartType.BATTERY,
    }
)
ROM_SIZES = MappingProxyType(
    {
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
    }
)
RAM_SIZES = MappingProxyType(
    {
        0x00: 0x0000,
        0x01: 0x0002,
        0x02: 0x0008,
        0x03: 0x0020,
        0x04: 0x0080,
        0x05: 0x0200,
    }
)
NUMBER_OF_RAM_BANKS = MappingProxyType(
    {
        0x00: 0,
        0x01: 1,
        0x02: 1,
        0x03: 4,
        0x04: 16,
        0x05: 8,
    }
)
NUMBER_OF_ROM_BANKS = MappingProxyType(
    {
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
    }
)
DESTINATION_CODES = MappingProxyType(
    {
        0x00: "Japanese",
        0x01: "Non-Japanese",
    }
)
