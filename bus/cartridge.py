from functools import reduce

from bus import Bank
from constants import CartridgeRanges, OLD_LICENSEE_CODES, NEW_LICENSEE_CODES, CARTRIDGE_TYPES, ROM_SIZES, RAM_SIZES, \
    NUM_RAM_BANKS, NUM_ROM_BANKS, DESTINATION_CODES


class Cartridge:
    data: bytearray
    rom_bank_0: Bank
    rom_bank_n: tuple[Bank]
    ram_bank: tuple[Bank]
    ram_enabled: bool = False
    cur_rom_bank: int = 1
    cur_ram_bank: int = 0

    @classmethod
    def load_from_file(cls, path) -> 'Cartridge':
        with open(path, 'rb') as f:
            return cls(bytearray(f.read()))

    def __init__(self, data: bytearray):
        super().__init__(data)
        self.rom_bank_0 = Bank(self.data[0x0000:0x4000])
        self.rom_bank_n = tuple(Bank(self.data[0x4000 * i:0x4000 * (i + 1)]) for i in range(1, self.num_rom_banks))
        self.ram_bank = tuple(Bank.of_len(0x2000) for _ in range(self.num_ram_banks))

    def _get_as_ascii(self, start, end):
        return self.data[start:end].decode('ascii')

    title = property(lambda self: self._get_as_ascii(*CartridgeRanges.TITLE.value).strip('\0').title())

    old_licensee_code = property(lambda self: OLD_LICENSEE_CODES.get(
            self.data[CartridgeRanges.OLD_LICENSEE_CODE.value[0]], 'Unknown').strip('\0'))

    new_licensee_code = property(lambda self: NEW_LICENSEE_CODES.get(
            self.data[CartridgeRanges.NEW_LICENSEE_CODE.value[0]], 'Unknown').strip('\0'))

    sgb_flag = property(lambda self: bool(self.data[CartridgeRanges.SGB_FLAG.value[0]]))
    cgb_flag = property(lambda self: bool(self.data[CartridgeRanges.CGB_FLAG.value[0]]))

    cartridge_type = property(lambda self: CARTRIDGE_TYPES.get(
        self.data[CartridgeRanges.CARTRIDGE_TYPE.value[0]], 'Unknown'))

    rom_size = property(lambda self: ROM_SIZES.get(self.data[CartridgeRanges.ROM_SIZE.value[0]], 'Unknown'))
    ram_size = property(lambda self: RAM_SIZES.get(self.data[CartridgeRanges.RAM_SIZE.value[0]], 'Unknown'))

    num_ram_banks = property(lambda self: NUM_RAM_BANKS.get(self.data[0x149], 0))
    num_rom_banks = property(lambda self: NUM_ROM_BANKS.get(self.data[0x148], 0))

    destination_code = property(lambda self: DESTINATION_CODES.get(
        self.data[CartridgeRanges.DESTINATION_CODE.value[0]], 'Unknown'))

    header_checksum = property(lambda self: self.data[CartridgeRanges.HEADER_CHECKSUM.value[0]])

    raw = property(lambda self: self.data)

    @property
    def passes_header_checksum(self):
        return reduce(lambda x, y: x - y - 1, self.data[0x134:0x14D], 0) & 0xFF == self.header_checksum

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
        return f'Cartridge()'

    def hex_view(self):
        out = ''
        for i in range(0, len(self.data), 16):
            out += f'{i:04X}  '
            for j in range(16):
                out += f'{self.data[i + j]:02X} '
            out += "  "
            for j in range(16):
                out += chr(self.data[i + j] if 0x20 <= self.data[i + j] <= 0x7E else 0x2E)
            out += '\n'
        return out