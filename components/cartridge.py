from dataclasses import dataclass, field
from pprint import pprint

from components import constants


@dataclass
class Cartridge:
    rom_data: bytearray = field(init=False, repr=False)

    def __init__(self, rom_path):
        self.rom_path = rom_path
        with open(rom_path, 'rb') as rom_file:
            self.rom_data = bytearray(rom_file.read())

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
        return 'Japanese' if self.rom_data[constants.CartridgeRanges.DESTINATION_CODE.value[0]] == 0 else 'Non-Japanese'

    def raw(self):
        return self.rom_data

    def __str__(self):
        return f'''Title: {self.title}
Old Licensee Code: {self.old_licensee_code}
New Licensee Code: {self.new_licensee_code}
SGB Flag: {self.sgb_flag}
CGB Flag: {self.cgb_flag}
Cartridge Type: {self.cartridge_type}
ROM Size: {self.rom_size}
RAM Size: {self.ram_size}
Destination Code: {self.destination_code}'''

    def __repr__(self):
        return f'Cartridge({repr(self.rom_path)})'


test = Cartridge('pb.gb')
print(str(test))

