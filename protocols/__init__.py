from typing import Protocol, Callable, Generator

# these are here to provide type hints and runtime checking if needed without having
# reliance on concrete classes as I wish to use a purely composition based approach to the project,
# which hopefully should allow me to make tests easily

read_address = Callable[[int, int], int]
write_address = Callable[[int, int], None]


class PPU(Protocol):
    read: Callable[[int, int], int]


class Timer(Protocol):
    pass


class Bank(Protocol):
    read: read_address
    write: write_address


class Cartridge(Protocol):
    read: read_address
    write: write_address


class Bus:
    read: Callable[[str], int | bool | None]
    write: Callable[[str, int], None]


class CPU(Protocol):
    interrupts_enabled: bool
    run: Callable[[Bus], Generator[int, int, None]]


class Register(Protocol):
    read: Callable[[str], int]
    write: Callable[[str, int], None]
