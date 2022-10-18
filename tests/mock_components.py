from typing import Generator

from protocols import BusProtocol


class MockMemoryBank:
    def read(self, address: int) -> int:
        return 0

    def write(self, address: int, value: int) -> None:
        ...


class MockPPU:
    def read(self, address: int, length: int) -> int:
        return 0

    def write(self, address: int, value: int) -> None:
        ...


class MockRegister:
    def read(self, address: str) -> int:
        return 0

    def write(self, address: str, value: int) -> None:
        ...


class MockBus:
    def read(self, address, length=1):
        return 0

    def write(self, address, value):
        pass

    def fetch8(self):
        return 0

    def fetch16(self):
        return 0

    def read_address(self, address, length=1):
        return 0

    def write_address(self, address, value):
        pass

    def run(self) -> Generator[int, int, None]:
        yield 0


class MockCPU:
    interrupts_enabled = False

    def run(self, bus: BusProtocol) -> Generator[int, int, None]:
        ...
