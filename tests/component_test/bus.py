from typing import Generator

from components.bus import Bus
from components.cartridge import Cartridge
from components.cpu import CPU
from components.register import Register

from tests.mock_components import MockBank, MockCPU, MockPPU, MockRegister
import pytest


def test_reg_8():
    bus = Bus(ppu=MockPPU(), register=Register(), wram=MockBank(), hram=MockBank(), cpu=MockCPU())

    assert bus.read('A') == 0x01
    bus.write('A', 0x02)
    assert bus.read('A') == 0x02

    assert bus.read('B') == 0x00
    bus.write('B', 0x02)
    assert bus.read('B') == 0x02

    assert bus.read('C') == 0x13
    bus.write('C', 0x02)
    assert bus.read('C') == 0x02

    assert bus.read('D') == 0x00
    bus.write('D', 0x02)
    assert bus.read('D') == 0x02

    assert bus.read('E') == 0xD8
    bus.write('E', 0x02)
    assert bus.read('E') == 0x02

    assert bus.read('F') == 0xB0
    bus.write('F', 0x02)
    assert bus.read('F') == 0x02

    assert bus.read('H') == 0x01
    bus.write('H', 0x02)
    assert bus.read('H') == 0x02

    assert bus.read('L') == 0x4D
    bus.write('L', 0x02)
    assert bus.read('L') == 0x02


def test_reg_16():
    bus = Bus(ppu=MockPPU(), register=Register(), wram=MockBank(), hram=MockBank(), cpu=MockCPU())

    assert bus.read('PC') == 0x100
    bus.write('PC', 0x200)
    assert bus.read('PC') == 0x200

    assert bus.read('SP') == 0xFFFE
    bus.write('SP', 0x200)
    assert bus.read('SP') == 0x200

    assert bus.read('AF') == 0x01B0
    bus.write('AF', 0x0303)
    assert bus.read('AF') == 0x0303
    assert bus.read('A') == 0x03
    assert bus.read('F') == 0x03

    assert bus.read('BC') == 0x0013
    bus.write('BC', 0x0303)
    assert bus.read('BC') == 0x0303
    assert bus.read('B') == 0x03
    assert bus.read('C') == 0x03

    assert bus.read('DE') == 0x00D8
    bus.write('DE', 0x0303)
    assert bus.read('DE') == 0x0303
    assert bus.read('D') == 0x03
    assert bus.read('E') == 0x03

    assert bus.read('HL') == 0x014D
    bus.write('HL', 0x0303)
    assert bus.read('HL') == 0x0303
    assert bus.read('H') == 0x03
    assert bus.read('L') == 0x03


def test_reg_8_invalid():
    register = Register()
    bus = Bus(ppu=MockPPU(), register=register, wram=MockBank(), hram=MockBank(), cpu=MockCPU())
    # todo, implement the raises in the code, and test it here


def test_reg_16_invalid():
    register = Register()
    bus = Bus(ppu=MockPPU(), register=register, wram=MockBank(), hram=MockBank(), cpu=MockCPU())
    # todo, implement the raises in the code, and test it here
