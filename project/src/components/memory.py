from array import array
from collections import namedtuple
from struct import pack, unpack
from project.src.system import data_distributor as dd

class Memory(array):
    offset: int

    def __init__(self, /, offset: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = offset

    def __getitem__(self, index: int):
        return super().__getitem__(index - self.offset)

    def __setitem__(self, index: int, value):
        super().__setitem__(index - self.offset, value)

Cartridge = namedtuple('Cartridge', ['rom_0', 'rom_N', 'ram'])




