import constants
from bus import Bank


class MMU:
    vram: Bank = Bank.of_len(len(constants.MemoryMapRanges.VRAM))
    wram: Bank = Bank.of_len(len(constants.MemoryMapRanges.WRAM))
    hram: Bank = Bank.of_len(len(constants.MemoryMapRanges.HRAM))

    def read_address(self, address, length=1):
        # more of these need to be implemented, these are sitting here as an example of how to implement them
        match address:
            case constants.MemoryMapRanges.VRAM | constants.MemoryMapRanges.WRAM | constants.MemoryMapRanges.HRAM:
                return getattr(self, address.name.lower()).read(address - address.start, length)
            case _:
                print(f'Unimplemented read from address {address:04X}')
                return 0

    def write_address(self, address, value):
        match address:
            # more of these need to be implemented, these are sitting here as an example of how to implement them
            case constants.MemoryMapRanges.VRAM | constants.MemoryMapRanges.WRAM | constants.MemoryMapRanges.HRAM:
                getattr(self, address.name.lower()).write(address - address.start, value)

            case None:
                print(f'Not an address {address}, this means something has failed.')
            case _:
                print(f'Unimplemented write to address {address:04X}')
