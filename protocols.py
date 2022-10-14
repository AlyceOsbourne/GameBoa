from typing import Protocol, Callable, Generator, runtime_checkable

# these are here to provide type hints and runtime checking if needed without having
# reliance on concrete classes as I wish to use a purely composition based approach to the project,
# which hopefully should allow me to make tests easily

read_address = Callable[[int, int], int]
write_address = Callable[[int, int], None]

@runtime_checkable
class PPU(Protocol):
    read: Callable[[int, int], int]
    write: Callable[[int, int], None]

@runtime_checkable
class Timer(Protocol):
    pass

@runtime_checkable
class Bank(Protocol):
    read: read_address
    write: write_address

@runtime_checkable
class Cartridge(Protocol):
    read: read_address
    write: write_address

@runtime_checkable
class Bus(Protocol):
    read: Callable[[str], int | bool | None]
    write: Callable[[str, int], None]
    fetch8: Callable[[], int]
    fetch16: Callable[[], int]
    read_address: read_address
    write_address: write_address
    request_interrupt: Callable[[int], None]


@runtime_checkable
class CPU(Protocol):
    interrupts_enabled: bool
    run: Callable[[Bus], Generator[int, int, None]]

@runtime_checkable
class Register(Protocol):
    read: Callable[[str], int]
    write: Callable[[str, int], None]
