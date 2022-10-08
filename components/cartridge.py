from dataclasses import dataclass
from pprint import pprint

from components import constants


@dataclass
class Cartridge:
    rom_data: bytearray

    def __init__(self, rom_path):
        with open(rom_path, 'rb') as rom_file:
            self.rom_data = bytearray(rom_file.read())

    @property
    def title(self):
        start, end =  constants.CartridgeRanges.TITLE
        return self.rom_data[start:end].decode('ascii')

    @property
    def cgb_flag(self):
        start, end = constants.CartridgeRanges.
        return self.rom_data[start:end]


if __name__ == "__main__":
    cart = Cartridge('Tetris.gb')
    # print the attrs of the Cartridge class
    pprint({
        attr.name: getattr(cart, attr.name.lower())
        for attr in constants.CartridgeRanges
    })
