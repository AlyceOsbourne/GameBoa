from components.bus import Bank
import components.system_mappings as system_mappings


class PPU:
    vram: Bank = Bank(len(system_mappings.MemoryMapRanges.VRAM))
    oam: Bank = Bank(len(system_mappings.MemoryMapRanges.OAM_RAM))
    lcdc: int = 0
    stat: int = 0
    scy: int = 0
    scx: int = 0
    ly: int = 0
    lyc: int = 0
    dma: int = 0
    bgp: int = 0
    obp0: int = 0
    obp1: int = 0
    wy: int = 0
    wx: int = 0

    def read(self, address, length=1):
        match address:
            case system_mappings.MemoryMapRanges.VRAM:
                """Reads from the VRAM"""
                return self.vram.read(address - address.start, length)
            case system_mappings.MemoryMapRanges.OAM:
                """Reads from the OAM"""
                return self.oam.read(address - address.start, length)
            case (
                system_mappings.MemoryMapRanges.LCDC |
                system_mappings.MemoryMapRanges.STAT |
                system_mappings.MemoryMapRanges.SCY |
                system_mappings.MemoryMapRanges.SCX |
                system_mappings.MemoryMapRanges.LY |
                system_mappings.MemoryMapRanges.LYC |
                system_mappings.MemoryMapRanges.DMA |
                system_mappings.MemoryMapRanges.BGP |
                system_mappings.MemoryMapRanges.OBP0 |
                system_mappings.MemoryMapRanges.OBP1 |
                system_mappings.MemoryMapRanges.WY |
                system_mappings.MemoryMapRanges.WX
            ):
                """Reads from the PPU"""
                return getattr(self, address.name.lower())
            case _:
                raise ValueError(f'Invalid address {address}')

    def write(self, address, value):
        match address:
            case system_mappings.MemoryMapRanges.VRAM:
                """Writes to the VRAM"""
                self.vram.write(address - address.start, value)
            case system_mappings.MemoryMapRanges.OAM:
                """Writes to the OAM"""
                self.oam.write(address - address.start, value)
            case (
                system_mappings.MemoryMapRanges.LCDC |
                system_mappings.MemoryMapRanges.STAT |
                system_mappings.MemoryMapRanges.SCY |
                system_mappings.MemoryMapRanges.SCX |
                system_mappings.MemoryMapRanges.LY |
                system_mappings.MemoryMapRanges.LYC |
                system_mappings.MemoryMapRanges.DMA |
                system_mappings.MemoryMapRanges.BGP |
                system_mappings.MemoryMapRanges.OBP0 |
                system_mappings.MemoryMapRanges.OBP1 |
                system_mappings.MemoryMapRanges.WY |
                system_mappings.MemoryMapRanges.WX
            ):
                """Writes to the PPU"""
                setattr(self, address.name.lower(), value)
            case _:
                raise ValueError(f'Invalid address {address}')
