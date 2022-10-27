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
    HRAM = 0xFF80, 0xFFFF
    ECHO = 0xE000, 0xFE00
    VRAM = 0x8000, 0xA000
    WRAM = 0xC000, 0xE000

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


    def __init__(self):
        self.hram = Memory(127)
        self.wram = Memory(8192)
        self.vram = Memory(8192)
        self.oam = Memory(160)
        self.cart = None
        EventHandler.subscribe(ComponentEvents.RomUnloaded, self.reset)
        EventHandler.subscribe(ComponentEvents.RomLoaded, self.load_rom)

    def reset(self):
        self.hram = Memory(127)
        self.wram = Memory(8192)
        self.vram = Memory(8192)
        self.oam = Memory(160)
        self.cart = Memory(33554432)
        EventHandler.publish(ComponentEvents.MemoryLoaded)

    def load_rom(self, rom: Path):
        self.cart = Memory(rom)
        EventHandler.publish(ComponentEvents.MemoryLoaded)

    def write_memory_address(self, address: int, value: bytes):
        match address:
            case MemoryRange.HRAM:
                rng = MemoryRange.HRAM
                mem = self.hram
            case MemoryRange.ECHO:
                rng = MemoryRange.WRAM
                mem = self.wram
            case MemoryRange.VRAM:
                rng = MemoryRange.VRAM
                mem = self.vram
            case MemoryRange.WRAM:
                rng = MemoryRange.WRAM
                mem = self.wram
            case _:
                raise NotImplementedError(f"Cannot write to address {address}")
        offset = address - rng.start
        end = offset + len(value)
        mem[offset:end] = value

    def read_memory_address(self, address: int, size) -> int:
        match address:
            case MemoryRange.HRAM:
                rng = MemoryRange.HRAM
                mem = self.hram
            case MemoryRange.ECHO:
                rng = MemoryRange.WRAM
                mem = self.wram
            case MemoryRange.VRAM:
                rng = MemoryRange.VRAM
                mem = self.vram
            case MemoryRange.WRAM:
                rng = MemoryRange.WRAM
                mem = self.wram
            case _:
                raise NotImplementedError(f"Cannot read from address {address}")
        offset = address - rng.start
        end = offset + size
        return  mem[offset:end]

    @EventHandler.subscriber(ComponentEvents.RequestMemoryRead)
    def requested_read(self, address: int, size: int, callback):
        callback(self.read_memory_address(address, size))

    @EventHandler.subscriber(ComponentEvents.RequestMemoryWrite)
    def rerquested_write(self, address: int, value: bytes):
        self.write_memory_address(address, value)









