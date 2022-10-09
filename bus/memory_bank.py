class Bank:
    """Holds the memory banks for the gameboy, this can be cartridge, vram, wram, etc"""
    data: bytearray

    def __init__(self, data: bytearray):
        self.data = data

    def read(self, address: int, length):
        return self.data[address:address + length]

    def write(self, address: int, value: int):
        self.data[address] = value

    @classmethod
    def of_len(cls, length: int) -> 'Bank':
        return cls(bytearray(length))