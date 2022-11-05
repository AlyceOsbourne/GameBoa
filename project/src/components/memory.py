import struct
from collections import namedtuple
from enum import Flag, auto
from types import MappingProxyType

from project.src.system import LogEvent, ComponentEvents, GuiEvents

LogEvent.LogInfo("Initializing Memory")
from array import array
from struct import pack, unpack

# we want to unpack the rom data as unsigned bytes, into the various rom banks depending on the cartridge type


class Memory:
    data: array
    start_offset: int


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


HEADER_FORMAT = (
    ("entrypoint", "4s"),
    ("logo", "48s"),
    ("title", "11s"),
    ("manufacturer_code", "4s"),
    ("cgb_flag", "B"),
    ("new_licensee_code", "2s"),
    ("sgb_flag", "B"),
    ("cartridge_type", "B"),
    ("rom_size", "B"),
    ("ram_size", "B"),
    ("destination_code", "B"),
    ("old_licensee_code", "B"),
    ("mask_rom_version", "B"),
    ("header_checksum", "B"),
    ("global_checksum", "H"),
)
HEADER_SIZE = sum(struct.calcsize(f[1]) for f in HEADER_FORMAT)
HEADER_START = 0x100
HEADER_END = HEADER_START + HEADER_SIZE
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
RAM_SIZES = MappingProxyType({0x00: 0x0000, 0x01: 0x0002, 0x02: 0x0008, 0x03: 0x0020, 0x04: 0x0080, 0x05: 0x0200})
DESTINATION_CODES = MappingProxyType(
    {
        0x00: "Japanese",
        0x01: "Non-Japanese",
    }
)
ROM_BANK_SIZE = 0x4000
RAM_BANK_SIZE = 0x2000
ROM_BANK_START = 0x4000
ROM_BANK_END = 0x8000
RAM_BANK_START = 0xA000
RAM_BANK_END = 0xC000
HeaderData = namedtuple("HeaderData", [f[0] for f in HEADER_FORMAT])


def calculate_checksum(compare: int, rom):
    """Calculate the checksum for the given ROM."""
    sum = 0
    for i in range(0x134, 0x14D):
        sum -= rom[i] + 1
    return sum & 0xFF == compare


def get_header_data(rom: array):
    mapping = {
        k: v
        for k, v in zip(
            [f[0] for f in HEADER_FORMAT],
            struct.unpack_from("<" + "".join(f[1] for f in HEADER_FORMAT), rom[HEADER_START:HEADER_END]),
        )
    }
    mapping["title"] = mapping["title"].decode("ascii").rstrip("\0").title()
    mapping["cartridge_type"] = CARTRIDGE_TYPES[mapping["cartridge_type"]]
    mapping["rom_size"] = ROM_SIZES[mapping["rom_size"]]
    mapping["ram_size"] = RAM_SIZES[mapping["ram_size"]]
    mapping["destination_code"] = DESTINATION_CODES[mapping["destination_code"]]
    mapping["old_licensee_code"] = OLD_LICENSEE_CODES.get(mapping["old_licensee_code"], "Unknown")
    mapping["new_licensee_code"] = NEW_LICENSEE_CODES.get(mapping["new_licensee_code"], "Unknown")
    # header checksum is sum all the header bytes together except the checksum bytes
    mapping["header_checksum"] = calculate_checksum(mapping["header_checksum"], rom)
    header_data = HeaderData(**mapping)
    LogEvent.LogDebug(f"ROM Header Data: {header_data}")
    ComponentEvents.HeaderLoaded(header_data)
    return header_data


class Cart:
    header: HeaderData
    rom_0: array
    rom_n: list[array]
    ram: list[array]
    ram_enabled: bool
    rom_bank: int
    ram_bank: int
    ram_mode: bool
