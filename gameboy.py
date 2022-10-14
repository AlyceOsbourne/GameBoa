from components.cpu import CPU
from components.memory_bank import Bank
from components.ppu import PPU
from components.register import Register
from components.timer import Timer
from components.bus import Bus
from components.system_mappings import Instruction

instr, cb_instr = Instruction.load_instructions().values()


class GameBoy:
    """The main gameboy class, this constructs all of the componets and triggers all of the systems"""

    def __init__(self):
        self.ppu = PPU()
        self.cpu = CPU(instr, cb_instr)
        self.register = Register()
        self.timer = Timer()
        self.wram = Bank(0x2000)
        self.hram = Bank(0x7F)
        self.bus = Bus(
            self.ppu,
            self.register,
            self.wram,
            self.hram,
            self.cpu,
            self.timer
        )


    def run(self):
        cpu_coro = self.cpu.run(self.bus)
        timer_coro = self.timer.run(self.bus)
        next(cpu_coro)
        while True:
            current_instr = self.bus.fetch8()
            cycles = cpu_coro.send(current_instr)
            timer_coro.send(cycles)
