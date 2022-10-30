from array import array
from collections import namedtuple
from struct import pack, unpack
from enum import Enum
from project.src.system.observer import Observer
from project.src.system.event_handler import EventHandler
from project.src.system.events import ComponentEvents, GuiEvents, SystemEvents


# 0000	3FFF	16KB ROM bank 00	From cartridge, usually a fixed bank
# 4000	7FFF	16KB ROM Bank 01~NN	From cartridge, switchable bank via MBC (if any)
# 8000	9FFF	8KB Video RAM (VRAM)	Only bank 0 in Non-CGB mode
# Switchable bank 0/1 in CGB mode
#
# A000	BFFF	8KB External RAM	In cartridge, switchable bank if any
# C000	CFFF	4KB Work RAM (WRAM) bank 0
# D000	DFFF	4KB Work RAM (WRAM) bank 1~N	Only bank 1 in Non-CGB mode
# Switchable bank 1~7 in CGB mode
#
# E000	FDFF	Mirror of C000~DDFF (ECHO RAM)	Typically not used
# FE00	FE9F	Sprite attribute table (OAM)
# FEA0	FEFF	Not Usable
# FF00	FF7F	I/O Registers
# FF80	FFFE	High RAM (HRAM)
# FFFF	FFFF	Interrupts Enable Register (IE)

# we now want to emulate the structure of the memory mappings
# we will use an Enum to store the memory mappings



class MemoryMap(namedtuple("MemoryMapping", ["start", "end"]), Enum):
    ROM = 0x0000, 0x7FFF
    VRAM = 0x8000, 0x9FFF
    EXTERNAL_RAM = 0xA000, 0xBFFF
    WRAM = 0xC000, 0xDFFF
    ECHO_RAM = 0xE000, 0xFDFF
    OAM = 0xFE00, 0xFE9F
    IO_REGISTERS = 0xFF00, 0xFF7F
    HRAM = 0xFF80, 0xFFFE
    INTERRUPT_ENABLE = 0xFFFF, 0xFFFF

    def __contains__(self, address):
        return self.start <= address <= self.end

    def __eq__(self, other):
        if isinstance(other, int):
            return other in self
        return super().__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return self.end - self.start + 1

    def __hash__(self):
        return hash(self.name) + hash(self.start) + hash(self.end)


working_ram = array("B", [0] * len(MemoryMap.WRAM))
video_ram = array("B", [0] * len(MemoryMap.VRAM))
external_ram = array("B", [0] * len(MemoryMap.EXTERNAL_RAM))
echo_ram = array("B", [0] * len(MemoryMap.ECHO_RAM))
oam = array("B", [0] * len(MemoryMap.OAM))
hram = array("B", [0] * len(MemoryMap.HRAM))
interrupt_enable = array("B", [0] * len(MemoryMap.INTERRUPT_ENABLE))

@EventHandler.subscriber(ComponentEvents.RequestMemoryWrite)
def write_memory(address, value):
    match address:
        case MemoryMap.WRAM:
            working_ram[address - MemoryMap.WRAM.start] = value
        case MemoryMap.VRAM:
            video_ram[address - MemoryMap.VRAM.start] = value
        case MemoryMap.EXTERNAL_RAM:
            external_ram[address - MemoryMap.EXTERNAL_RAM.start] = value
        case MemoryMap.ECHO_RAM:
            echo_ram[address - MemoryMap.ECHO_RAM.start] = value
        case MemoryMap.OAM:
            oam[address - MemoryMap.OAM.start] = value
        case MemoryMap.HRAM:
            hram[address - MemoryMap.HRAM.start] = value
        case MemoryMap.INTERRUPT_ENABLE:
            interrupt_enable[address - MemoryMap.INTERRUPT_ENABLE.start] = value
        case _:
            raise ValueError(f"Address {address} is not a valid memory address")


@Observer.observable(ComponentEvents.RequestMemoryRead)
def read_memory(address):
    match address:
        case MemoryMap.WRAM:
            return working_ram[address - MemoryMap.WRAM.start]
        case MemoryMap.VRAM:
            return video_ram[address - MemoryMap.VRAM.start]
        case MemoryMap.EXTERNAL_RAM:
            return external_ram[address - MemoryMap.EXTERNAL_RAM.start]
        case MemoryMap.ECHO_RAM:
            return echo_ram[address - MemoryMap.ECHO_RAM.start]
        case MemoryMap.OAM:
            return oam[address - MemoryMap.OAM.start]
        case MemoryMap.HRAM:
            return hram[address - MemoryMap.HRAM.start]
        case MemoryMap.INTERRUPT_ENABLE:
            return interrupt_enable[address - MemoryMap.INTERRUPT_ENABLE.start]
        case _:
            raise ValueError(f"Address {address} is not a valid memory address")