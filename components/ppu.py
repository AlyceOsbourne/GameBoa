from protocols import Bank
from components.memory_bank import MemoryBank
from components.system_mappings import PPUReadWriteRanges, ScreenSize


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
    oam: Bank = MemoryBank(len(PPUReadWriteRanges.OAM))
    vram: Bank = MemoryBank(len(PPUReadWriteRanges.VRAM))

    def read(self, address, length=1):
        addr_space = PPUReadWriteRanges.from_address(address)[0]

        match address:
            case (PPUReadWriteRanges.LY |
                    PPUReadWriteRanges.WX |
                    PPUReadWriteRanges.WY |
                    PPUReadWriteRanges.BGP |
                    PPUReadWriteRanges.DMA |
                    PPUReadWriteRanges.LYC |
                    PPUReadWriteRanges.SCX |
                    PPUReadWriteRanges.SCY |
                    PPUReadWriteRanges.LCDC |
                    PPUReadWriteRanges.OBP0 |
                    PPUReadWriteRanges.OBP1 |
                    PPUReadWriteRanges.STAT
            ):
                return getattr(self, addr_space.name.lower())
            case PPUReadWriteRanges.OAM | PPUReadWriteRanges.VRAM:
                offset = address - addr_space.start
                return getattr(self, addr_space.name.lower())[offset:offset + length]
            case _:
                raise ValueError(f"Invalid address {address}.")

    def write(self, address, *value: int):
        if len(value) == 0:
            raise ValueError("No value to write.")
        match address:
            case (PPUReadWriteRanges.LY |
                    PPUReadWriteRanges.WX |
                    PPUReadWriteRanges.WY |
                    PPUReadWriteRanges.BGP |
                    PPUReadWriteRanges.DMA |
                    PPUReadWriteRanges.LYC |
                    PPUReadWriteRanges.SCX |
                    PPUReadWriteRanges.SCY |
                    PPUReadWriteRanges.LCDC |
                    PPUReadWriteRanges.OBP0 |
                    PPUReadWriteRanges.OBP1 |
                    PPUReadWriteRanges.STAT
            ):
                addr_space = PPUReadWriteRanges.from_address(address)[0]
                offset = address - addr_space.start
                setattr(self, addr_space.name.lower(), value[offset])
            case PPUReadWriteRanges.OAM | PPUReadWriteRanges.VRAM:
                addr_space = PPUReadWriteRanges.from_address(address)
                offset = address - addr_space.start
                getattr(self, addr_space.name.lower())[offset:offset + len(value)] = value
            case _:
                raise ValueError(f"Invalid address {address}.")

    def run(self, bus):
        while True:
            if self.ly == 144:
                self.stat |= 0b00000001
                self.stat &= 0b11111110
                bus.interrupts.request_interrupt(0)
            elif self.ly < 144:
                self.stat |= 0b00000010
                self.stat &= 0b11111101
            else:
                self.stat |= 0b00000000
                self.stat &= 0b11111111
            self.ly += 1
            if self.ly > 153:
                self.ly = 0
            yield 456



class ScreenConsoleRenderer:
    # renders the PPUs screen to the console
    def __init__(self, screen_size: ScreenSize):
        self.screen_size = screen_size
        self.screen: list[list] = [[0 for _ in range(screen_size.width)] for _ in range(screen_size.height)]

    def render(self):
        for y in range(self.screen_size.height):
            for x in range(self.screen_size.width):
                print(self.screen[y][x], end="")
            print()

    def update(self, ppu):
        # update the screen
        for y in range(self.screen_size.height):
            for x in range(self.screen_size.width):
                pixel_value = ppu.read(0x8000 + y * self.screen_size.width + x)
                match pixel_value:
                    case 0:
                        pixel_char = " "
                    case 1:
                        pixel_char = "░"
                    case 2:
                        pixel_char = "▒"
                    case 3:
                        pixel_char = "▓"
                    case _:
                        raise ValueError(f"Invalid pixel value {pixel_value}.")
                self.screen[y][x] = pixel_char

    def run(self, ppu):
        while True:
            yield
            self.update(ppu)
            self.render()
