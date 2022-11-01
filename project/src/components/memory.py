from array import array
from collections import namedtuple
from struct import pack, unpack
from project.src.system import bus as dd

class Memory(array):
    # class to represent the memory of the game boy, this can be any of the internal memory,
    # the cartridge, the video ram, the work ram, etc.

    offset: int

    def __init__(self, /, offset: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = offset

    def __getitem__(self, index: int):
        return super().__getitem__(index - self.offset)

    def __setitem__(self, index: int, value):
        super().__setitem__(index - self.offset, value)

class _Cart:
    ...

class _SwitchableCart(_Cart):
    ...

class RomOnlyCart(_SwitchableCart):
    # class to represent a cartridge with no mappers
    ...

class MBC1Cart(_SwitchableCart):
    # class to represent a cartridge with MBC1 mapper
    ...

class MBC2Cart(_SwitchableCart):
    # class to represent a cartridge with MBC2 mapper
    ...

class MBC3Cart(_SwitchableCart):
    # class to represent a cartridge with MBC3 mapper
    ...






