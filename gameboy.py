from components.cpu import CPU
from components.memory_bank import Bank
from components.ppu import PPU
from components.register import Register
from components.timer import Timer
from components.bus import Bus
from components.system_mappings import Instruction

instructions, cb_instructions = Instruction.load_instructions().values()


class GameBoy:
    """The main gameboy class, this constructs all of the componets and triggers all of the systems"""

    def __init__(self):
        self.ppu = PPU()
        self.cpu = CPU(instructions, cb_instructions)
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
