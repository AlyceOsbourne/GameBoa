from typing import Any

from protocols import Cartridge, CPU, Bank, PPU, Register, Timer
from components.system_mappings import (
    Interrupts,
    PPUReadWriteRanges,
    CartridgeReadWriteRanges,
)


class Bus:
    """The main bus that manages data throughput."""

    __slots__ = ("cart", "cpu", "hram", "ime", "ppu", "register", "timer", "wram")

    def __init__(
        self,
        cpu: CPU,
        ppu: PPU,
        hram: Bank,
        wram: Bank,
        timer: Timer,
        register: Register,
        cart: Cartridge | None = None,
    ):
        self.cpu = cpu
        self.ppu = ppu
        self.cart = cart
        self.hram = hram
        self.ime = False
        self.wram = wram
        self.register = register

    def fetch8(self) -> int:
        """Fetches 8 bits from the current program counter."""
        value = self.read_address(self.read("PC"))
        self.register.write("PC", self.read("PC") + 1)
        return value

    def fetch16(self) -> int:
        """Fetches 16 bits from the current program counter."""
        value = self.read_address(self.read("PC"), 2)
        self.register.write("PC", self.read("PC") + 2)
        return value

    def push(self, value: int) -> None:
        """Pushes a value onto the stack pointer."""
        self.write("SP", self.read("SP") - 2)
        self.write_address(self.read("SP"), value)

    def pop(self) -> int:
        """Pops a value from the stack pointer."""
        value = self.read_address(self.read("SP"), 2)
        self.write("SP", self.read("SP") + 2)
        return value

    def read(self, operator: str) -> int | bool | None:
        """Reads a memory address of the given operator."""
        match operator:
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10" | "11" | "12" | "13" | "14" | "15":
                return int(operator)
            case "d16" | "a16":
                return self.read_address(self.read("PC"), 2)
            case "d8" | "a8" | "r8":
                return self.read_address(self.read("PC"))
            case "PC" | "SP" | "A" | "B" | "C" | "D" | "E" | "F" | "H" | "L" | "AF" | "BC" | "DE" | "HL":
                return self.register.read(operator)
            case "(BC)" | "(DE)" | "(HL)" | "(C)" | "(a16)" | "(a8)":
                return self.read_address(self.read(operator[1:-1]))
            case "HL+" | "HL-":
                value = self.read("HL")
                self.register.write(
                    "HL", self.read("HL") + 1 if operator == "HL+" else -1
                )
                return value
            case "(HL+)" | "(HL-)":
                return self.read_address(self.read(operator[1:-1]), 1)
            case "SP+r8":
                return self.register.read("SP") + self.read("d8")
            case "Z":
                return self.register.read("F") & 0b10000000
            case "NZ":
                return not self.register.read("F") & 0b10000000
            case "NC":
                return not self.register.read("F") & 0b00010000
            case None:
                return None
            case _:
                print(f"Unimplemented read from operator {operator}.")
                return None

    def write(self, operator: str, value: Any):
        match operator:
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10" | "11" | "12" | "13" | "14" | "15":
                self.register.write("F", self.register.read("F") | (1 << int(operator)))
            case "PC" | "SP" | "A" | "B" | "C" | "D" | "E" | "F" | "H" | "L" | "AF" | "BC" | "DE" | "HL":
                self.register.write(operator, value)
            case "(BC)" | "(DE)" | "(HL)" | "(C)" | "(a16)" | "(a8)" | "(HL+)" | "(HL-)":
                self.write_address(self.read(operator[1:-1]), value)
            case "d8":
                self.write_address(self.read("PC"), value)
            case _:
                print(f"Unimplemented write to operator {operator}.")

    def read_address(self, address: int, length: int = 1):
        """Reads memory data from the given address."""
        match address:
            case (
                CartridgeReadWriteRanges.ROM_BANK_0
                | CartridgeReadWriteRanges.ROM_BANK_N
            ) if self.cart is not None:
                return self.cart.read(address, length)
            case (PPUReadWriteRanges.OAM | PPUReadWriteRanges.VRAM):
                return self.ppu.read(address, length)
            case _:
                print(f"Unimplemented read from address {address}.")
                return 0xFF

    def write_address(self, address: int, value: int):
        """Writes memory data to the given address."""
        match address:
            case (
                CartridgeReadWriteRanges.ROM_BANK_0
                | CartridgeReadWriteRanges.ROM_BANK_N
            ) if self.cart is not None:
                self.cart.write(address, value)
            case (PPUReadWriteRanges.VRAM | PPUReadWriteRanges.OAM):
                self.ppu.write(address, value)
            case _:
                print(f"Unimplemented write to address {address}.")

    def request_interrupt(self, interrupt: int):
        """Requests an interrupt."""
        self.hram.write(0xFF0F, self.hram.read(0xFF0F, 1) | interrupt)

    def handle_interrupts(self):
        """Handles multiple interrupts."""
        if self.ime:
            interrupt = self.hram.read(0xFF0F, 1) & self.hram.read(0xFFFF, 1)

            if interrupt:
                self.ime = False
                self.hram.write(0xFF0F, self.hram.read(0xFF0F, 1) & ~interrupt)
                self.push(self.read("PC"))

                match interrupt:
                    case 0b00000001:
                        self.write("PC", 0x0040)
                    case 0b00000010:
                        self.write("PC", 0x0048)
                    case 0b00000100:
                        self.write("PC", 0x0050)
                    case 0b00001000:
                        self.write("PC", 0x0058)
                    case 0b00010000:
                        self.write("PC", 0x0060)
                    case _:
                        print(f"Unimplemented interrupt {interrupt}.")
