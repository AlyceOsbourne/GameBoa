from typing import Any
from pathlib import Path
from functools import reduce, singledispatchmethod

from components import system_mappings
from components.memory_bank import MemoryBank
from components.system_mappings import (
    RAM_SIZES,
    ROM_SIZES,
    CARTRIDGE_TYPES,
    DESTINATION_CODES,
    NEW_LICENSEE_CODES,
    OLD_LICENSEE_CODES,
    NUMBER_OF_RAM_BANKS,
    NUMBER_OF_ROM_BANKS,
    CartridgeHeaderRanges,
)


class Cartridge:
    data: bytearray
    rom_bank_0: MemoryBank
    current_ram_bank: int = 0
    current_rom_bank: int = 1
    ram_enabled: bool = False
    ram_bank: tuple[MemoryBank, ...]
    rom_bank_n: tuple[MemoryBank, ...]

    @singledispatchmethod
    def __init__(self, data):
        ...

    @__init__.register(bytearray)
    def from_byte_array(self, data):
        self.data = data
        self.rom_bank_0 = MemoryBank(self.data[0x0000:0x4000])
        self.rom_bank_n = tuple(
            MemoryBank(self.data[0x4000 * i : 0x4000 * (i + 1)])
            for i in range(1, self.number_of_rom_banks)
        )
        self.ram_bank = tuple(MemoryBank(0x2000) for _ in range(self.number_of_ram_banks))

    @__init__.register(Path)
    @__init__.register(str)
    def from_file(self, file):
        with open(file, "rb") as f:
            self.__init__(bytearray(f.read()))

    def _get_as_ascii(self, start, end):
        return self.data[start:end].decode("ascii")

    def read(self, address, length: int= 1):
        match address:
            case system_mappings.CartridgeReadWriteRanges.ROM_BANK_0:
                return self.rom_bank_0.read(address, length)

            case _:
                print(f"Unimplemented read from cartridge {address}.")
                return 0

    def write(self, address, *value: int):
        match address:

            case _:
                print(f"Unimplemented write to cartridge {address}.")

    title = property(
        lambda self: self._get_as_ascii(*CartridgeHeaderRanges.TITLE.value)
        .strip("\0")
        .title()
    )

    old_licensee_code = property(
        lambda self: OLD_LICENSEE_CODES.get(
            self.data[CartridgeHeaderRanges.OLD_LICENSEE_CODE.value[0]], "Unknown"
        ).strip("\0")
    )

    new_licensee_code = property(
        lambda self: NEW_LICENSEE_CODES.get(
            self.data[CartridgeHeaderRanges.NEW_LICENSEE_CODE.value[0]], "Unknown"
        ).strip("\0")
    )

    sgb_flag = property(
        lambda self: bool(self.data[CartridgeHeaderRanges.SGB_FLAG.value[0]])
    )
    cgb_flag = property(
        lambda self: bool(self.data[CartridgeHeaderRanges.CGB_FLAG.value[0]])
    )

    cartridge_type = property(
        lambda self: CARTRIDGE_TYPES.get(
            self.data[CartridgeHeaderRanges.CARTRIDGE_TYPE.value[0]], "Unknown"
        )
    )

    rom_size = property(
        lambda self: ROM_SIZES.get(
            self.data[CartridgeHeaderRanges.ROM_SIZE.value[0]], "Unknown"
        )
    )
    ram_size = property(
        lambda self: RAM_SIZES.get(
            self.data[CartridgeHeaderRanges.RAM_SIZE.value[0]], "Unknown"
        )
    )

    number_of_ram_banks = property(
        lambda self: NUMBER_OF_RAM_BANKS.get(self.data[0x149], 0)
    )
    number_of_rom_banks = property(
        lambda self: NUMBER_OF_ROM_BANKS.get(self.data[0x148], 0)
    )

    destination_code = property(
        lambda self: DESTINATION_CODES.get(
            self.data[CartridgeHeaderRanges.DESTINATION_CODE.value[0]], "Unknown"
        )
    )

    header_checksum = property(
        lambda self: self.data[CartridgeHeaderRanges.HEADER_CHECKSUM.value[0]]
    )

    raw = property(lambda self: self.data)

    @property
    def passes_header_checksum(self):
        return (
            reduce(lambda x, y: x - y - 1, self.data[0x134:0x14D], 0) & 0xFF
            == self.header_checksum
        )

    def __str__(self):
        return (
            f"Title: {self.title}\n"
            f"CGB Flag: {self.cgb_flag}\n"
            f"RAM Size: {self.ram_size}\n"
            f"ROM Size: {self.rom_size}\n"
            f"SGB Flag: {self.sgb_flag}\n"
            f"Cartridge Type: {self.cartridge_type}\n"
            f"Header Checksum: {self.header_checksum}\n"
            f"Destination Code: {self.destination_code}\n"
            f"New Licensee Code: {self.new_licensee_code}\n"
            f"Old Licensee Code: {self.old_licensee_code}\n"
            f"Number of RAM Banks: {self.number_of_ram_banks}\n"
            f"Number of ROM Banks: {self.number_of_rom_banks}\n"
            f"Passes Header Checksum: {self.passes_header_checksum}\n"
        )

    def __repr__(self):
        return f"Cartridge()"

    def hex_output(self):
        output = ""

        for i in range(0, len(self.data), 16):
            output += f"{i:04X}  "

            for j in range(16):
                output += f"{self.data[i + j]:02X} "

            output += "  "

            for j in range(16):
                output += chr(
                    self.data[i + j] if 0x20 <= self.data[i + j] <= 0x7E else 0x2E
                )

            output += "\n"

        return output
