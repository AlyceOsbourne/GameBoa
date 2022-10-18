from components.bus import Bus
from components.ppu import PPU
from components.memory_bank import MemoryBank
from components.system_mappings import Instruction


INSTRUCTIONS, CB_INSTRUCTIONS = Instruction.load().values()


class GameBoy:
    """All essential components and a trigger for all the systems."""

    def __init__(self):
        self.ppu = PPU()
        self.timer = Timer()
        self.register = Register()
        self.hram = MemoryBank(0x7F)
        self.wram = MemoryBank(0x2000)
        self.cpu = CPU(INSTRUCTIONS, CB_INSTRUCTIONS)
        self.bus = Bus(
            cpu=self.cpu,
            ppu=self.ppu,
            hram=self.hram,
            wram=self.wram,
            timer=self.timer,
            register=self.register,
        )

    def run(self) -> None:
        cpu_coroutine = self.cpu.run(self.bus)
        timer_coroutine = self.timer.run(self.bus)
        next(cpu_coroutine)

        while True:
            current_instruction = self.bus.fetch8()
            cycles = cpu_coroutine.send(current_instruction)
            timer_coroutine.send(cycles)
