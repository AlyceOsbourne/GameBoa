"""
Factory functions for components.

Named as ..._manager(). Maybe they should be named as ..._factory() or
even as ..._provider()?

Not sure about their proper name. I'm not even sure if this is how this
should be done.

The three dots in, for example, Bus(...) indicate that the arguments are
not yet given.
"""


from bus import Bus
from cpu import CPU
from ppu import PPU
from timer import Timer
from register import Register


def bus_manager() -> Bus:
    return Bus(...)


def cpu_manager() -> CPU:
    return CPU(...)


def ppu_manager() -> PPU:
    return PPU(...)


def timer_manager() -> Timer:
    return Timer(...)


def register_manager() -> Register:
    return Register(...)

