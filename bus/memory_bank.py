class Bank:
    """Holds the memory banks for the gameboy, this can be cartridge, vram, wram, etc"""
    data: bytearray

    def __init__(self, data: bytearray):
        self.data = data

    def read(self, address: int, length):
        """Returns the value at address"""
        return self.data[address:address + length]

    def write(self, address: int, value: int):
        """Writes the value to the address"""
        self.data[address] = value

    @classmethod
    def of_len(cls, length: int) -> 'Bank':
        """Creates a bank of a certain length"""
        return cls(bytearray(length))

    def __len__(self):
        """Size of the bank"""
        return len(self.data)

    def hex_view(self, start: int, end: int) -> str:
        """Returns a hex view of the bank"""
        output = ''
        for i in range(start, end):
            if i % 16 == 0:
                output += f'{i:04X} '
            output += f'{self.data[i]:02X} '
            if i % 16 == 15:
                output += '\n'
        return output
