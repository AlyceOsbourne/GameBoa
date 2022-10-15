from components.bus import Bus
from components.ppu import PPU
from components.memory_bank import Bank
from components.system_mappings import Instructions


INSTRUCTIONS, CB_INSTRUCTIONS = Instructions.load().values()


class GameBoy:
    """
    The main composite class of the GameBoa application.

    It includes all required components and triggers all systems.
    """

    def __init__(self):
        self.ppu = PPU()
        self.cpu = CPU(INSTRUCTIONS, CB_INSTRUCTIONS)
        self.register = Register()
        self.timer = Timer()
        self.wram = Bank(0x2000)
        self.hram = Bank(0x7F)
        self.bus = Bus(
            self.ppu, self.register, self.wram, self.hram, self.cpu, self.timer
        )

    def run(self) -> None:
        cpu_coroutine = self.cpu.run(self.bus)
        timer_coroutine = self.timer.run(self.bus)
        next(cpu_coroutine)

        while True:
            current_instruction = self.bus.fetch8()
            cycles = cpu_coroutine.send(current_instruction)
            timer_coroutine.send(cycles)
