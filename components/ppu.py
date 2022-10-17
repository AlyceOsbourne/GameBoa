from protocols import MemoryBank


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
    oam: MemoryBank
    vram: MemoryBank

    def read(self, address, length=1):
        match address:
            case _:
                raise ValueError(f"Invalid address {address}.")

    def write(self, address, value):
        match address:
            case _:
                raise ValueError(f"Invalid address {address}.")
