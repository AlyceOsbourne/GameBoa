from functools import singledispatchmethod


class Bank:
    """Manages the memory bank of the Game Boy."""

    data: bytearray

    @singledispatchmethod
    def __init__(self, data):
        raise NotImplementedError

    @__init__.register(int)
    def sized(self, size: int):
        """Creates a bank of the given size."""
        self.data = bytearray(size)

    @__init__.register(bytearray)
    def from_bytearray(self, data: bytearray):
        """Creates a bank from the given data."""
        self.data = data

    def read(self, address: int, length: int = 1) -> int:
        """Returns the value of the given address."""
        return self.data[address : address + length]

    def write(self, address: int, value: int):
        """Writes the given value to the given address."""
        self.data[address] = value

    def __len__(self):
        """Retuns the size of a bank."""
        return len(self.data)

    def hex_view(self, start: int, end: int) -> str:
        """Returns the hex view of a bank."""
        output = ""

        for i in range(start, end):
            if i % 16 == 0:
                output += f"{i:04X} "
            output += f"{self.data[i]:02X} "

            if i % 16 == 15:
                output += "\n"

        return output
