from protocols import Bank
from components.memory_bank import MemoryBank
from components.system_mappings import PPUReadWriteRanges


OAM_RANGE = len(PPUReadWriteRanges.OAM)
VRAM_RANGE = len(PPUReadWriteRanges.VRAM)


class PPU:
    ly: int = 0
    wx: int = 0
    wy: int = 0
    bgp: int = 0
    dma: int = 0
    lyc: int = 0
    scx: int = 0
    scy: int = 0
    lcdc: int = 0
    obp0: int = 0
    obp1: int = 0
    stat: int = 0
    oam: Bank = MemoryBank(OAM_RANGE)
    vram: Bank = MemoryBank(VRAM_RANGE)

    def read(self, address, length: int = 1):
        """Reads the given address."""
        match address:
            case _:
                raise ValueError(f"Invalid address {address}.")

    def write(self, address, value: int):
        match address:
            case _:
                raise ValueError(f"Invalid address {address} with value {value}.")
