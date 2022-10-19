from typing import Callable, Generator, Protocol, runtime_checkable

from components.system_mappings import Instructions

ReadAddress = Callable[[int, int], int]
WriteAddress = Callable[[int, int], None]


@runtime_checkable
class PPU(Protocol):
    read: ReadAddress
    write: WriteAddress
    run: Callable[["Bus"], Generator[int, None, None]]


@runtime_checkable
class Timer(Protocol):
    run: Callable[['Bus'], Generator[None, int, None]]


@runtime_checkable
class Bank(Protocol):
    read: ReadAddress
    write: WriteAddress


@runtime_checkable
class Cartridge(Protocol):
    read: ReadAddress
    write: WriteAddress


@runtime_checkable
class Bus(Protocol):
    read: Callable[[str], int | bool | None]
    write: Callable[[str, int], None]
    fetch8: Callable[[], int]
    fetch16: Callable[[], int]
    read_address: ReadAddress
    write_address: WriteAddress
    request_interrupt: Callable[[int], None]


@runtime_checkable
class CPU(Protocol):
    interrupts_enabled: bool
    run: Callable[[Bus], Generator[int, int, None]]
    decode: Callable[[int], Instructions]
    execute: Callable[[Bus, int], int]


@runtime_checkable
class Register(Protocol):
    read: Callable[[str], int]
    write: Callable[[str, int], None]
