from dataclasses import dataclass

from constants import cartridge_types


@dataclass
class Cartridge:
    rom_data: bytearray

    def __init__(self, rom_path):
        with open(rom_path, 'rb') as rom_file:
            self.rom_data = bytearray(rom_file.read())

    @property
    def title(self):
        return self.rom_data[0x134:0x143].decode('ascii').strip('\x00').title()

    @property
    def sgb_flag(self):
        return self.rom_data[0x146] == 0x03

    @property
    def cgb_flag(self):
        return self.rom_data[0x143] in (0x80, 0xC0)

    @property
    def cartridge_type(self):
        return cartridge_types.get(self.rom_data[0x147], 'Unknown')

    @property
    def rom_size(self):
        return 32 << self.rom_data[0x148]

    @property
    def ram_size(self):
        return 32 << self.rom_data[0x149]

    @property
    def header_checksum(self):
        return self.rom_data[0x14D]

    @property
    def has_camera(self):
        return self.rom_data[0x147] == 0xFC

    @property
    def has_rumble(self):
        return self.rom_data[0x147] == 0xFD

    @property
    def has_bluetooth(self):
        return self.rom_data[0x147] == 0xFE

    @property
    def has_multicart(self):
        return self.rom_data[0x147] == 0xFF

    @property
    def has_battery(self):
        return self.rom_data[0x147] in [0x03, 0x06, 0x09, 0x0D, 0x0F, 0x10, 0x13, 0x1B, 0x1E, 0x22, 0xFC, 0xFD, 0xFE,
                                        0xFF]

    @property
    def has_timer(self):
        return self.rom_data[0x147] in [0x0F, 0x10, 0x13, 0x1E, 0xFF]

    @property
    def has_rtc(self):
        return self.rom_data[0x147] in [0x0F, 0x10, 0x13, 0x1E, 0xFF]

    @property
    def has_tama5(self):
        return self.rom_data[0x14B] == 0x33

    @property
    def has_mbc(self):
        return self.rom_data[0x147] in [0x01, 0x02, 0x03, 0x05, 0x06, 0x08, 0x09, 0x0B, 0x0C, 0x0D, 0x0F, 0x10, 0x12,
                                        0x13, 0x1B, 0x1E, 0x22, 0xFC, 0xFD, 0xFE, 0xFF]

    def hex_table(self, start_address: int, end_address: int):
        hex_view = ''
        if start_address % 16 != 0:
            start_address -= start_address % 16
        if end_address % 16 != 0:
            end_address += 16 - (end_address % 16)
        for i in range(start_address, end_address, 16):
            hex_view += f'{i:04X}  '
            for j in range(16):
                hex_view += f'{self.rom_data[i + j]:02X} '
            hex_view += ' '
            for j in range(16):
                hex_view += chr(self.rom_data[i + j]) if 32 <= self.rom_data[i + j] <= 126 else '.'
            hex_view += '\n'
        return hex_view

    mem_view = property(lambda self: self.hex_table(0x00, len(self.rom_data)))

    def read_rom(self, address:int):
        return self.rom_data[address]

    def write_rom(self, address:int, value:int):
        self.rom_data[address] = value

