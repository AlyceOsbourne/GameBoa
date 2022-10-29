import array
from collections import namedtuple
from enum import Enum
from functools import singledispatchmethod
from pathlib import Path
from typing import Any


from project.src.system.event_handler import EventHandler
from project.src.system.events import SystemEvents, GuiEvents, ComponentEvents

class _MemoryRange(namedtuple("MemoryRange", "start end")):
    def __contains__(self, item):
        return self.start <= item < self.end

class MemoryRange(_MemoryRange, Enum):
    CART = 0x0000, 0x8000
    HRAM = 0xFF80, 0xFFFF
    ECHO = 0xE000, 0xFE00
    VRAM = 0x8000, 0xA000
    WRAM = 0xC000, 0xE000

    @classmethod
    def get_from_addr(cls, addr):
        for memory_range in cls:
            if addr in memory_range:
                return memory_range
        raise ValueError(f"Address {addr} not in any memory range")

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

    def write_addr(self, addr: int, data: bytes):
        self.data[addr : addr + len(data)] = array.array("B", data)

    def read_addr(self, addr: int, size: int) -> bytes:
        return bytes(self.data[addr : addr + size])

class MemoryManagementUnit:

    def __init__(self):
        self.hram = Memory(127)
        self.wram = Memory(8192)
        self.echo = self.wram
        self.vram = Memory(8192)
        self.oam = Memory(160)
        self.cart = Memory(0x8000)
        EventHandler.subscribe(ComponentEvents.RomUnloaded, self.reset)
        EventHandler.subscribe(ComponentEvents.RomLoaded, self.load_rom)
        EventHandler.subscribe(ComponentEvents.RequestMemoryRead, self.requested_read_memory_address)
        EventHandler.subscribe(ComponentEvents.RequestMemoryWrite, self.write_memory_address)
        EventHandler.subscribe(GuiEvents.RequestMemoryStatus, self.requested_status)
        EventHandler.subscribe(ComponentEvents.RequestReset, self.reset)

    def reset(self):
        self.hram = Memory(127)
        self.wram = Memory(8192)
        self.vram = Memory(8192)
        self.oam = Memory(160)
        self.cart = None

    def load_rom(self, rom):
        self.cart = Memory(rom)

    def write_memory_address(self, address: int, data: bytes):
        rng = MemoryRange.get_from_addr(address)
        if not rng:
            raise ValueError(f"Address {address} not in any memory range")
        getattr(self, rng.name.lower()).write_addr(address, data)

    def read_memory_address(self, address: int, length):
        rng = MemoryRange.get_from_addr(address)
        if not rng:
            raise ValueError(f"Address {address} not in any memory range")
        return getattr(self, rng.name.lower()).read_addr(address, length)

    def requested_read_memory_address(self, address: int, length: int, callback):
        callback(self.read_memory_address(address, length))

    def requested_status(self, callback):
        callback(str(self))









