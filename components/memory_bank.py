from functools import singledispatchmethod


class MemoryBank:
    """An emulation of a memory bank."""

    data: bytearray

    @singledispatchmethod
    def __init__(self, data):
        self.data = data

    @__init__.register(int)
    def sized(self, size: int) -> None:
        """Creates a memory bank of the given size."""
        self.data = bytearray(size)

    @__init__.register(bytearray)
    def from_bytearray(self, data: bytearray) -> None:
        """Creates a memory bank from the given data as a bytearray."""
        self.data = data

    def read(self, address: int, length: int = 1) -> bytearray:
        """Returns a value of the given address."""
        return self.data[address : (address + length)]

    def write(self, address: int, value: int) -> None:
        """Writes the given value to the given address."""
        self.data[address] = value
    def __len__(self):
        """Returns the size of a memory bank."""
        return len(self.data)

    def hex_output(self, start: int, end: int) -> str:
        """Returns the hex value of a memory bank."""
        output = ""

        for i in range(start, end):
            if i % 16 == 0:
                output += f"{i:04X} "
            output += f"{self.data[i]:02X} "

            if i % 16 == 15:
                output += "\n"

        return output
