from components.bus import Bus
from components.ppu import PPU
from components.memory_bank import MemoryBank
from components.system_mappings import Instruction


INSTRUCTIONS, CB_INSTRUCTIONS = Instruction.load().values()


class GameBoy:
    """
    The main class of GameBoa.

    It includes all essential components and triggers all systems.
    """

    def __init__(self):
        self.ppu = PPU()
        self.timer = Timer()
        self.hram = Bank(0x7F)
        self.wram = Bank(0x2000)
        self.register = Register()
        self.cpu = CPU(INSTRUCTIONS, CB_INSTRUCTIONS)
        self.bus = Bus(
            self.cpu, self.ppu, self.hram, self.wram, self.timer, self.register
        )

    def run(self) -> None:
        cpu_coroutine = self.cpu.run(self.bus)
        timer_coroutine = self.timer.run(self.bus)
        next(cpu_coroutine)

        while True:
            current_instruction = self.bus.fetch8()
            cycles = cpu_coroutine.send(current_instruction)
            timer_coroutine.send(cycles)
