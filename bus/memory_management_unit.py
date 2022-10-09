from bus import Bank


class MMU:
    vram: Bank
    wram: Bank
    sram: Bank
    hram: Bank
    oam: Bank

    def read_address(self, address, length=1):
        match address:
            case _:
                print(f'Unimplemented read from address {address:04X}')

    def write_address(self, address, value):
        match address:
            case _:
                print(f'Unimplemented write to address {address:04X}')