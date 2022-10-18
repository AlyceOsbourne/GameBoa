from typing import Callable, Generator, Protocol, runtime_checkable


ReadAddress = Callable[[int, int], int]
WriteAddress = Callable[[int, int], None]


@runtime_checkable
class PPUProtocol(Protocol):
    read: ReadAddress
    write: WriteAddress


@runtime_checkable
class TimerProtocol(Protocol):
    ...


@runtime_checkable
class MemoryBankProtocol(Protocol):
    read: ReadAddress
    write: WriteAddress


@runtime_checkable
class CartridgeProtocol(Protocol):
    read: ReadAddress
    write: WriteAddress


@runtime_checkable
class BusProtocol(Protocol):
    read: Callable[[str], int | bool | None]
    write: Callable[[str, int], None]
    fetch8: Callable[[], int]
    fetch16: Callable[[], int]
    read_address: ReadAddress
    write_address: WriteAddress
    request_interrupt: Callable[[int], None]


@runtime_checkable
class CPUProtocol(Protocol):
    interrupts_enabled: bool
    run: Callable[[BusProtocol], Generator[int, int, None]]


@runtime_checkable
class RegisterProtocol(Protocol):
    read: Callable[[str], int]
    write: Callable[[str, int], None]
