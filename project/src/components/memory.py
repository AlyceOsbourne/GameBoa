import array, struct
from collections import namedtuple
from enum import Enum
from functools import singledispatchmethod
from pathlib import Path
from typing import Any

class Memory:
    data: array.array

    @singledispatchmethod
    def __init__(self, d: Any):
        raise TypeError(f"Cannot initialize memory with {d} of type {type(d)}")

    @__init__.register(int)
    def _of_size(self, size: int):
        self.data = array.array("B", [0] * size)

    @__init__.register(Path)
    def _from_file(self, path: Path):
        self.data = array.array("B", path.read_bytes())

    @__init__.register(array.array)
    def _from_array(self, data: array.array):
        self.data = data

    @__init__.register(bytes)
    def _from_bytes(self, data: bytes):
        self.data = array.array("B", data)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


    def __getitem__(self, item: int | slice) -> int | array.array:
        if isinstance(item, slice):
            return array.array("B", self.data[item])
        return self.data[item]

    def __setitem__(self, key: int, value: int):
        self.data[key] = value

    def __setslice__(self, i, j, sequence):
        self.data[i:j] = sequence

class MemoryManagementUnit:
    # cart cane be of varying sizes, we buffer with null bytes
    HRAM = Memory(127)
    WRAM = Memory(8192)
    VRAM = Memory(8192)
    OAM = Memory(160)
    # cart rom big enough to account for all possible sizes of carts aka 32mb
    cart = Memory(33554432)












